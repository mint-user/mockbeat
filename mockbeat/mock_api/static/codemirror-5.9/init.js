(function(){
    var $ = django.jQuery;
    $(document).ready(function(){
        $('textarea.html-editor').each(function(idx, el){
            CodeMirror.fromTextArea(el, {
                lineNumbers: true,
                mode: 'python',
                theme: "default",
                setSize: {
                    width: 800,
                    height: 600
                },
            });
        });
    });
})();
