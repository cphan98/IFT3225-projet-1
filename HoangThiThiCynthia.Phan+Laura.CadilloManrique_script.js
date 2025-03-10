document.querySelectorAll('.clickable').forEach(row => {
    row.addEventListener('mousedown', function() {
        let mediaSrc = this.getAttribute('data-src');
        let mediaType = this.getAttribute('data-type');
        let popupContent = document.getElementById('popup-content');
        let popup = document.getElementById('popup');
        if (mediaType === "IMAGE") {
            popupContent.innerHTML = `<img src="${mediaSrc}" alt="Popup Image">`;
        } else if (mediaType === "VIDEO") {
            popupContent.innerHTML = `<video controls><source src="${mediaSrc}" type="video/mp4"></video>`;
        }
        popup.style.display = 'block';
    });
    row.addEventListener('mouseup', function() {
        document.getElementById('popup').style.display = 'none';
    });
});