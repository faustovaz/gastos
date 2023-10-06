(function(){

    document.addEventListener('DOMContentLoaded', function(){
        var elements = document.querySelectorAll(".sidenav");
        var instances = M.Sidenav.init(elements, {});

        var btns = document.querySelectorAll('.fixed-action-btn');
        var btnsInstances = M.FloatingActionButton.init(btns, {direction: 'left', 
            hoverEnabled: true, 
            toolbarEnabled: true});
    });

})();
