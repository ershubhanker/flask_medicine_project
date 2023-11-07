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
    
    updateList();  // Update the list to include the new entry
    $('#autocomplete1').val('');  // Clear the input for a new entry
  },
});

function updateList() {
    $('#added-drugs-ol').empty();

      // Toggle the 'No meds added yet' text visibility
    if (selectedNames.length === 0) {
        $('#no-meds-text').show(); // Show the placeholder when there are no meds
    } else {
        $('#no-meds-text').hide(); // Hide the placeholder when there are meds
    }

    // Repopulate the added drugs list using the updated selectedNames array
    selectedNames.forEach(function(name, index) {
      var listItem = $(`<li class="drug-item">${index + 1}. ${name}<a href="#" class="remove-tag">✖</a></li>`);
      $('#added-drugs-ol').append(listItem);
      // Event listener to remove items from the added drugs list
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

$('#submit-button').on('click', function(e) {
    e.preventDefault(); // Prevent the default form submission
    var pcids = selectedPCIDs.join(','); // Join the PCIDs into a single string separated by commas
  
    $.ajax({
      url: `/interactions?pcids=${pcids}`,
      type: 'GET',
      success: function(response) {
        // This function will handle the response
        displayInteractions(response.interactions);
      },
      error: function(error) {
        console.log('Error:', error);
        // Handle error
        // You may want to display an error message to the user
      }
    });
  });
  
  function displayInteractions(interactions) {
    var container = $('#interaction-data-container');
    container.empty(); // Clear any previous data
  
    // Loop through the interactions and create a box for each
    interactions.forEach(function(interaction) {
      var box = $('<div class="interaction-box"></div>');
      box.append(`<p><strong>Description:</strong> ${interaction.description}</p>`);
      box.append(`<p><strong>Extended Description:</strong> ${interaction.extended_description}</p>`);
      box.append(`<p><strong>Severity:</strong> ${interaction.severity}</p>`);
      box.append(`<p><strong>Evidence Level:</strong> ${interaction.evidence_level}</p>`);
      box.append(`<p><strong>Management:</strong> ${interaction.management}</p>`);
      container.append(box);
    });
  }
  