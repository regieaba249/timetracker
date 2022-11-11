$(document).on("click", ".open-modal-btn", function () {
     var url = this.getAttribute('data-url')
     var name = this.getAttribute('data-name')

     $("#ss_modal img").attr("src", url);
     $("#ss_modal exampleModalLabel").innerHTML = name;

});