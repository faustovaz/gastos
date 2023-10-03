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


    document.addEventListener('DOMContentLoaded', function() {
        let chip = document.querySelectorAll('.chips');
        let chipInstance = M.Chips.init(chip, 
            { 
                placeholder: 'Tags',
                limit: 5,
                onChipAdd: function() {
                    let tagsField = document.querySelector("#tags")
                    tagsField.value = this.chipsData.map(chip => chip.tag).join(";")
                },
                onChipDelete: function(evt) {
                    let tagsField = document.querySelector("#tags")
                    tagsField.value = this.chipsData.map(chip => chip.tag).join(";")
                },
            }
        );
        let tags = document.querySelector("#tags").value.trim();
        if (tags) {
            let chipElement = M.Chips.getInstance(document.querySelector('.chips'));
            tags.split(";").forEach(tag => {
                chipElement.addChip({tag: tag});
            });
        }
        let parceladoCheck = document.querySelector("#parcelado")
        hideOrShowIf(parceladoCheck.checked, document.querySelector("#parcelas").closest('li'));
    });
})();
