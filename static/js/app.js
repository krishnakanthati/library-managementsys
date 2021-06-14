const search = () => {
    let filter = document.getElementById('myInput').value.toUpperCase();
    let myDiv = document.getElementById('myDiv')
    let section = myDiv.getElementsByTagName('section')
    for (var i = 0; i < section.length; i++) {
        let h5 = section[i].getElementsByTagName('h5')[0]

        if (h5) {
            let textvalue = h5.textContent || h5.innerHTML
            if (textvalue.toUpperCase().indexOf(filter) > -1) {
                section[i].style.display = ""
            } else {
                section[i].style.display = "none"
            }
        }
    }
}