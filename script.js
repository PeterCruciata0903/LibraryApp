/* DEFAULT API CALL fetch("https://www.googleapis.com/books/v1/volumes?q=a&orderBy=") //replace q with search query 
.then((response) => {
    if(response.ok)
    {
        return response.json();
    }
    else{
        throw new Error("Network Response error")
    }
})
.then(data => {
    console.log(data.items[0]);
})
.catch((error) => console.error("FETCH ERROR:", error)); */

function getBook(data)
{
    const div = document.getElementById("result");

    //deletes old searches if they exist
    if(div.hasChildNodes())
    {
        while (div.firstChild) {
            div.removeChild(div.firstChild);
        }
    }
    //using HTML DOM get data from api and append it to HTML
    for(let i = 0; i < 25; i++)
    {
    const name = data.items[i].volumeInfo.title;
    const writer = data.items[i].volumeInfo.authors;
    const publisher= data.items[i].volumeInfo.publisher;
    const publishedDate=data.items[i].volumeInfo.publishedDate;
    const description=data.items[i].volumeInfo.description;
    const pageCount=data.items[i].volumeInfo.pageCount;

 
    const heading = document.createElement("h2");
    const heading2 = document.createElement("h3");
    const heading3=document.createElement("h3");
    const heading4=document.createElement("h3");
    const heading5=document.createElement("h4");
    const heading6=document.createElement("h3");
    const bookimg = document.createElement("img");
   
    bookimg.onclick = function() {
        window.location.href = data.items[i].volumeInfo.canonicalVolumeLink;
    };
    bookimg.setAttribute('title',"click for more info"); //very cool
    
    bookimg.src = data.items[i].volumeInfo.imageLinks.thumbnail;
    heading.innerHTML = "Title: "+name;
    heading2.innerHTML = "Author: "+ writer;
    heading3.innerHTML="Publisher: "+publisher;
    heading4.innerHTML="Published Date: "+publishedDate;
    heading6.innerHTML="Page Count: "+pageCount;
    heading5.innerHTML="Description: "+description;


    div.appendChild(bookimg);
    div.appendChild(heading);
    div.appendChild(heading2);
    div.appendChild(heading3);
    div.appendChild(heading4);
    div.appendChild(heading6);
    div.appendChild(heading5);


    }
    
}
//runs the api search with term passed in from the html input field in index.html
function apiSearch(term)
{
    
    fetch("https://www.googleapis.com/books/v1/volumes?q=" + term)
    .then((response) => {
        if(response.ok)
        {
            return response.json();
        }
        else{
            throw new Error("Network Response error")
        }
    })
    .then(data => {
        getBook(data)
    })
    .catch((error) => console.error("FETCH ERROR:", error));
}

//makes it so if enter is pressed it will still run the search
let input = document.getElementById("myform");
input.addEventListener("keypress", function(event)
{
    if(event.key === "Enter")
    {
        event.preventDefault();
    document.getElementById("searchbtn").click();
    }
});
