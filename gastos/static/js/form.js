(function(){
    
    let changeIfChecked = (source, target) => {
        if (source.checked) {
            target.checked = !source.checked;
        }
    };

    let hideOrShowIf = (show, target) => {
        show ? target.classList.remove("hide") : target.classList.add("hide");
    };


    document.querySelector("#parcelado").addEventListener('change', (evt) => {
        changeIfChecked(evt.currentTarget, document.querySelector("#recorrente"));
        hideOrShowIf(evt.currentTarget.checked, document.querySelector("#parcelas").closest('li'));
    });
    document.querySelector("#recorrente").addEventListener('change', (evt) => {
        let parceladoCheck = document.querySelector("#parcelado");
        changeIfChecked(evt.currentTarget, parceladoCheck);
        hideOrShowIf(parceladoCheck.checked, document.querySelector("#parcelas").closest('li'));
    });
})();
