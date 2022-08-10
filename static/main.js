
function runSuite(input){

}



function deleteChildren(){
    let parent = document.getElementById("going-to-practice");
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
    parent = document.getElementById("filled-form");
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
    parent = document.getElementById("strikes");
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }

}

function goingToPractice(text){
    let elt = document.getElementById("going-to-practice");
    if(text === ""){
        elt.innerHTML += "<br />";
        return;
    }
    elt.innerHTML += "<br />" + text;
}

function filledOutForm(text){
    let elt = document.getElementById("filled-form");
    if(text === ""){
        elt.innerHTML += "<br />";
        return;
    }
    elt.innerHTML += "<br />" + text;
}

function strikes(arr){
    let elt = document.getElementById("strikes");
    if(arr == "Strikes"){
        elt.innerHTML += "<br />" + "Strikes:";
        return;
    }
    if(arr == ""){
        elt.innerHTML += "<br />";
        return;
    }
    for(let strike of arr)
        elt.innerHTML += "<br />" + strike;
        
}

function displayTable(text){
    let elt = document.getElementById("table-wrapper");
    deleteChildren(elt);
    elt.innerHTML += text;
    makeTableContentEditable();
}

function setDateButtons(arr){
    let toggleButtonsElt = document.getElementById("button-toggle");
    deleteChildren(toggleButtonsElt);
    for(let date of arr){
        let newButton = document.createElement("button");
        newButton.innerHTML = date;
        newButton.class = "toggle-button"
        toggleButtonsElt.appendChild(newButton);
    }
}

function makeTableContentEditable(){
    let table = document.querySelector(".dataframe");
    for(let row of table.rows){
        for(let cell of row.cells){
            if(cell.innerHTML == "Yes" || cell.innerHTML == "No")
                cell.contentEditable = true;
        }
    }
    table.addEventListener('change', () => {
        //Update csv file via python
    })
}

document.getElementById("button-toggle").addEventListener("click", (e)=> {toggleActiveButton(e)})
curActive = null;

function toggleActiveButton(e){
    if(!(e.target instanceof HTMLButtonElement))
        return;
        
    deleteChildren();
    
    if(curActive)
        curActive.style.backgroundColor = "white";
    curActive = e.target
    curActive.style.backgroundColor = "grey";

}