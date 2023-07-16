function addPet() {
    var petType = document.getElementById("pet-type").value;
    var petList = document.getElementById("pet-list");
    var petItem = document.createElement("div");
    petItem.textContent = petType;
    petList.appendChild(petItem);
}
