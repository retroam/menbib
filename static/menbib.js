$(document).ready( function() {

    $('#select-all-checkbox').change(function(){
        if(this.checked){
            $('#all-items-table').find(':checkbox').prop('checked','checked');
        }
        else {
            $('#all-items-table').find(':checkbox').removeAttr('checked')
        }
    }
    )

}
);

function createmenbibCitation(citationStyle){
    selectedKeys = getSelectedKeys()

    $.ajax({
        type: 'POST',
        url: getmenbibCitationURL(),
        data: JSON.stringify({allKeys : selectedKeys, style : citationStyle}),
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            displaymenbibCitations(data, citationStyle)
        }
    });
}

function displaymenbibCitations(citationText, citationStyle){
    $('#citationModalTitle').html('Citations in \<i\>' + citationStyle + '\</i\> Style')
    $('#citationModalBody').html(citationText)
    $('#citationModal').modal('show')
}

function getSelectedKeys(){
    var selectedKeys = new Array()

    $('#all-items-table').find('input:checked').each(function(){
        if($(this).attr('name') != 'select-all'){
            selectedKeys.push($(this).attr('name'))
        }
    }
    )

    return selectedKeys;
}

function exportmenbibItems(format){
    selectedKeys = getSelectedKeys()

    var key_string = encodeURIComponent(selectedKeys.join())

    $.ajax({
        type: 'POST',
        url: getmenbibExportBaseURL(),
        data: JSON.stringify({allKeys : selectedKeys, format : format}),
        contentType: 'application/json',
        dataType: 'json',
        success: function(data) {
            //displayCitations(data[0]['citationText'], citationStyle)
        }
    });
}

function getmenbibExportURL(format){
    selectedKeys = getSelectedKeys()

    var baseURL = getmenbibExportBaseURL()

    baseURL += '?format='+format;

    for(var i = 0 ; i < selectedKeys.length; i++){
        baseURL += '&allKeys=' + selectedKeys[i]
    }

    return baseURL
}