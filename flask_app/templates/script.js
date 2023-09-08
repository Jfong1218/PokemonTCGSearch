console.log("hello script is working")
// URL = "https://api.pokemontcg.io/v2/cards"
URL = "https://api.pokemontcg.io/v2/cards?q=name:"

function getPoke(event){
    event.preventDefault()
    pokeResultDiv = document.querySelector('#pokeResult')
    pokeName = document.querySelector("#pokeName").value
    // pokeResultDiv.innerHTML="loading...."
    console.log("form submitted")
    console.log(pokeName)
    fetch(URL+pokeName)
        .then(response => response.json())
        .then (data => {
            console.log(data)
            console.log(data.data[0]["name"])
            var result = ""
            for(var i=0; i<data.data.length; i++){
                console.log(data.data[i].images.large);
                result += `
                <div class='row' id='card-container'>
                <h1>${data.data[i]["name"]}</h1>
                <img src="${data.data[i].images.large}"></img>
                </div>`
            }
            pokeResultDiv.innerHTML = `
                <div class="container">
                ${result}
                </div>
                `
        })
        .catch(err => console.log(err));
}

{/* <div class="container">
<div class='row' id='card-container'>

</div>
</div>  */}