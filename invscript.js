function table()
{
    //targets div table will be put into
    const div = document.getElementById("container");
    //makes table and the headers
    const table = document.createElement("table");
    const tr =  document.createElement("tr");
    const th =  document.createElement("th");
    const th2 =  document.createElement("th");
    const th3 =  document.createElement("th");

    
    //table header info
    th.innerHTML = "Title";
    th2.innerHTML = "Author";
    th3.innerHTML = "Availability";
    //appends header tto table
    tr.appendChild(th);
    tr.appendChild(th2);
    tr.appendChild(th3);
    table.appendChild(tr);

    //TO DO get data from database and place it in table
    //Availabliity text should have link to call reserve, return and check out functions
for(let i = 0; i <5;i++) 
{
    const tr2 =  document.createElement("tr");
    //table data
    const td =  document.createElement("td");
    const td2 =  document.createElement("td");
    const td3 =  document.createElement("td");
    //database data go here :)
    td.innerHTML = "Rocky part " + (i+1);
    td2.innerHTML = "Peter Griffin";
    td3.innerHTML = "Out of stock";
    tr2.appendChild(td);
    tr2.appendChild(td2);
    tr2.appendChild(td3);
    table.appendChild(tr2);
}
    //the table is appended to the div under the hero img
    div.appendChild(table);
}
