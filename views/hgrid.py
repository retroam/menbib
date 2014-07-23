
from framework import request
from website.project.decorators import must_be_contributor_or_public, must_have_addon
from website.addons.menbib.utils import folder_to_hgrid
from website.addons.menbib.client import get_node_client


@must_be_contributor_or_public
@must_have_addon('mendeley', 'node')
def menbib_hgrid_data_contents(node_addon, auth, **kwargs):
    """Return the Rubeus/HGrid-formatted response for a folder's contents.

    Takes optional query parameters `foldersOnly` (only return folders) and
    `includeRoot` (include the root folder).
    """
    # No folder, just return an empty list of data

    if node_addon.folder is None and not request.args.get('foldersOnly'):
        return {'data': []}

    # permissions = {
    #     'edit': node.can_edit(auth) and not node.is_registration,
    #     'view': node.can_view(auth)
    # }
    # client = get_node_client(node)
    # folders = client.folders()
    # if request.args.get('foldersOnly'):
    #     contents = [folder_to_hgrid(folder, node, permissions) for
    #                 folder in folders]
    # # TODO: In the future display folder contents?
    # else:
    #     contents = [folder_to_hgrid(folder, node, permissions) for
    #                 folder in folders]
    #
    # return contents
