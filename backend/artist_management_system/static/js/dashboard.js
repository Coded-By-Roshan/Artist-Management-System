function openTab(evt, tabId) {
    const contents = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-link');

    contents.forEach(content => content.classList.remove('active'));
    buttons.forEach(btn => btn.classList.remove('active'));

    document.getElementById(tabId).classList.add('active');
    evt.currentTarget.classList.add('active');
  }




const deleteLinks = document.querySelectorAll('#delete_user');

  deleteLinks.forEach(link => {
    link.addEventListener('click', function (event) {
      console.log("this is clicked")
      event.preventDefault(); 
      const url = this.getAttribute('data-url');
      console.log(url)
      if (confirm('Are you sure you want to delete this user?')) {
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