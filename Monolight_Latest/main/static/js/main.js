showDetail = event => {
    id1 = event.id;
    id2 = `${event.id}1`;
    var x = document.getElementById(event.id);
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
    var y = document.getElementById(id2);
    if (y.style.display === "none") {
        y.style.display = "block";
    } else {
        y.style.display = "none";
    }
};

