function IDValidator()
{
   
    id = document.getElementById("id").value;
    id = id.toString();
    if (id.length !== 9 || isNaN(id)) { 
        document.getElementById("demo").innerHTML = "the id must by 9 digits";
        return false;
    }
    let sum = 0, incNum;
    for (const i in id) {
        incNum = Number(id[i]) * ((i % 2) + 1);
        sum += (incNum > 9) ? incNum - 9 : incNum;  
    }
    document.getElementById("demo").innerHTML = "hello";
    return (sum % 10 === 0);
}