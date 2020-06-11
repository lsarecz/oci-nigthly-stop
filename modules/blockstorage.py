import oci

resource_name = 'block storage'

def change_block_volume_performance(config, signer, compartments):

    target_resources = []

    print("Listing all {}... (* is marked for performance change)".format(resource_name))
    for compartment in compartments:
        # print("  compartment: {}".format(compartment.name))
        resources = _get_resource_list(config, signer, compartment.id)
        for resource in resources:
            go = 0
            if (resource.lifecycle_state == 'AVAILABLE'):
                if ('Monitoring' in resource.defined_tags) and ('whitelisted' in resource.defined_tags['Monitoring']):
                    if (resource.defined_tags['Monitoring']['whitelisted'].upper() != 'YES'):
                        go = 1
                else:
                    go = 1

            if (go == 1):
                print("    * {} ({}) in {}".format(resource.display_name, resource.lifecycle_state, compartment.name))
                target_resources.append(resource)
            else:
                print("      {} ({}) in {}".format(resource.display_name, resource.lifecycle_state, compartment.name))

    print('\nUpdating parformance * marked {}...'.format(resource_name))
    for resource in target_resources:
        try:
            response = _change_blockstorage_performance(config, signer, resource.id, 0)
        except oci.exceptions.ServiceError as e:
            print("---------> error. status: {}".format(e))
            pass
        else:
            if response.lifecycle_state == 'PROVISIONING':
                print("    update requested: {} ({})".format(response.display_name, response.lifecycle_state))
            else:
                print("---------> not updated: {} ({})".format(response.display_name, response.lifecycle_state))

    print("\nAll {} updated!".format(resource_name))


def _get_resource_list(config, signer, compartment_id):
    object = oci.core.BlockstorageClient(config=config, signer=signer)
    resources = oci.pagination.list_call_get_all_results(
        object.list_volumes,
        compartment_id=compartment_id
    )
    return resources.data

def _change_blockstorage_performance(config, signer, resource_id, vpus_per_gb):
    object = oci.core.BlockstorageClient(config=config, signer=signer)
    volume = object.get_volume(resource_id)
    details = oci.core.models.UpdateVolumeDetails(vpus_per_gb = vpus_per_gb)
    if volume.data.vpus_per_gb > 0:
        response = object.update_volume(
            resource_id,
            details
        )
    else:
        response = object.get_volume(resource_id)
    return response.data
