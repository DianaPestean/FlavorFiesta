
  //GET SEARCH FORM AND PAGE LINKS
  let searchForm = document.getElementById('searchForm')
  let pageLinks = document.getElementsByClassName('page-link')

  //ENSURE SEARCH FORM EXISTS
  if(searchForm){
    for(let i=1; pageLinks.length > i; i++ ){
      pageLinks[i].addEventListener('click', function (e) {
        e.preventDefault()
        console.log('First step')

        //GET THE DATA ATTRIBUTE

        let page = this.dataset.page 
        console.log('Second step')

        //ADD HIDDEN SEARCH INPUT TO FORM
        searchForm.innerHTML += `<input value=${page} name="page" hidden />`
        console.log('Third step')


        // //SUBMIT FORM
        searchForm.submit()
        console.log('Fourth step')

      })
    }
  }
