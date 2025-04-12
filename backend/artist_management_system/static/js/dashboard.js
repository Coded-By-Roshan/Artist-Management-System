
function openTab(evt, tabName) {
  document.querySelectorAll(".tab-content").forEach(tab => {
    tab.classList.remove("active");
  });

  document.querySelectorAll(".tab-link").forEach(btn => {
    btn.classList.remove("active");
  });

  document.getElementById(tabName).classList.add("active");
  evt.currentTarget.classList.add("active");

}

window.onload = function () {
  const hash = window.location.hash.substring(1);
  if (hash) {
    const tab = document.getElementById(hash);
    const button = document.querySelector(`.tab-link[onclick*="${hash}"]`);
    if (tab && button) {
      button.click();
    }
  }
};



const deleteLinks = document.querySelectorAll('#delete_item');
  deleteLinks.forEach(link => {
    link.addEventListener('click', function (event) {
      console.log("this is clicked")
      event.preventDefault(); 
      const url = this.getAttribute('data-url');
      console.log(url)
      if (confirm('Are you sure you want to delete this item?')) {
        window.location.href = url; 
      }
    });
  });


const editButtons = document.querySelectorAll('.edit-btn');
editButtons.forEach(btn => {
    btn.addEventListener('click', function () {
        document.getElementById('edit-id').value = this.dataset.id;
        document.getElementById('edit-first_name').value = this.dataset.first_name;
        document.getElementById('edit-last_name').value = this.dataset.last_name;
        document.getElementById('edit-email').value = this.dataset.email;
        document.getElementById('edit-phone').value = this.dataset.phone;
        document.getElementById('edit-dob').value = this.dataset.dob;
        document.getElementById('edit-gender').value = this.dataset.gender;
        document.getElementById('edit-address').value = this.dataset.address;
    });
});


const artist_edit = document.querySelectorAll('.edit_artist');
artist_edit.forEach(btn => {
    btn.addEventListener('click', function () {
        document.getElementById('edit-aid').value = this.dataset.id;
        document.getElementById('edit-fullname').value = this.dataset.name;
        document.getElementById('edit-artist-dob').value = this.dataset.dob;
        document.getElementById('edit-artist-address').value = this.dataset.address;
        document.getElementById('edit-artist-gender').value = this.dataset.gender;
        document.getElementById('edit-release_year').value = this.dataset.first_release_year;
  
    });
});

const song_edit = document.querySelectorAll('.edit_song');
song_edit.forEach(btn => {
    btn.addEventListener('click', function () {
        document.getElementById('song_id').value = this.dataset.song_id;
        document.getElementById('artist_id').value = this.dataset.artist_id;
        console.log(this.dataset.song_id)
        console.log(this.dataset.artist_id)
        document.getElementById('edit-title').value = this.dataset.title;
        document.getElementById('edit-album_name').value = this.dataset.album_name;
        document.getElementById('edit-genre').value = this.dataset.genre;
  
    });
});

