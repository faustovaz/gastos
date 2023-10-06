(function(){

    document.addEventListener('DOMContentLoaded', function(){
        let elements = document.querySelectorAll(".sidenav");
        let instances = M.Sidenav.init(elements, {});

        let btn = document.querySelector('.fixed-action-btn');
        let floatingBtn = M.FloatingActionButton.init(btn);
        let opened = false;

        if (floatingBtn) {
            floatingBtn.el.addEventListener('click', (evt) => {
                opened ? floatingBtn.close() : floatingBtn.open();
                opened = !opened;
            });
   
        }
    });

})();
