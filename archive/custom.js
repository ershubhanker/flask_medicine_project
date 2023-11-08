// Inside your custom.js file
document.addEventListener('DOMContentLoaded', (event) => {
    // Get a reference to the component
    const medicationSearch = document.getElementsByName("medication-1")[0];
  
    // Attach a listener for the db-value-changed event
    medicationSearch.addEventListener("db-value-changed", function(e) {
      if (e.detail.drugbank_pcid) {
        // If a medication is selected, you could call a function to do something with the value
        handleSelectedMedication(e.detail.drugbank_pcid);
      } else {
        // Handle the case where the selection is cleared
        handleClearedSelection();
      }
    });
  });
  
  function handleSelectedMedication(drugbankPcid) {
    console.log(`Selected medication PCID: ${drugbankPcid}`);
    // Add your logic here to deal with the selected medication PCID
    // For example, you might want to save it to a variable, make an API call, or update the UI
  }
  
  function handleClearedSelection() {
    console.log("The medication selection has been cleared.");
    // Add your logic here to deal with the case when selection is cleared
  }
  