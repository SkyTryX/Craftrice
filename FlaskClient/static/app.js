const submit = document.getElementById("submit")
const input1 = document.getElementById("input1")
const input2 = document.getElementById("input2")
const warn = document.getElementById("warn")

function check(event){
    if(input1.value === "") event.preventDefault()
    if(input2.value === "") event.preventDefault()
    input1_content= Number(input1.value);
    input2_content= Number(input2.value);
    console.log(input1_content, input2_content)
    if(-7 > input1_content || input1_content > 7 || -7 > input2_content || input2_content > 7){
        console.log("4")
        event.preventDefault()
        submit.style.background= '#FF0000';
        warn.style.color = "#FF0000";
        console.log("5")
        //submit.style.background='#04AA6D';
    }
}

submit.addEventListener("click", check)