// Define arrays to store the names and PCIDs
var selectedNames = [];
var selectedPCIDs = [];

$('#autocomplete1').autocomplete({
  serviceUrl: '/search/names',
  dataType: 'json',
  minChars: 3,
  maxHeight: 300,
  onSelect: function (suggestion) {
    // Store the selected name and PCID into arrays
    selectedNames.push(suggestion.value);
    selectedPCIDs.push(suggestion.data.drugbank_pcid);

    console.log('Selected names:', selectedNames);  // Logging the names
    console.log('Selected PCIDs:', selectedPCIDs);  // Logging the PCIDs
    
    createTag(suggestion.value);  // Create a tag for the new entry
    $('#autocomplete1').val('');  // Clear the input for a new entry
  },
});

function createTag(name) {
  updateList(); // Update the list to include the new tag
}

function updateList() {
  $('#drugs-ol').empty(); // Clear the list
  // Repopulate it using the updated selectedNames array
  selectedNames.forEach(function(name, index) {
    var listItem = $(`<li class="drug-item">${index + 1}. ${name}<a href="#" class="remove-tag">✖</a></li>`);
    $('#drugs-ol').append(listItem);
    listItem.find('.remove-tag').click(function(e) {
      e.preventDefault();
      var itemIndex = listItem.index(); // Get the index before removing the item
      // Remove the name and PCID from the arrays
      selectedNames.splice(itemIndex, 1);
      selectedPCIDs.splice(itemIndex, 1);
      updateList(); // Update the list after removal
    });
  });
}
