window.onload = function () {
    console.log('pub_blog.js NEW VERSION')
    const { createEditor, createToolbar } = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default',
    })

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        mode: 'default',
    })

    $("#submit-bt").click(function (event){
        //阻止按钮的默认行为
        event.preventDefault();

        let title = $("input[name='title']").val();
        let category = $("select[name='category']").val();
        let content = editor.getHtml();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        $.ajax('/blog/pub',{
            method:'POST',
            data:{title,category,content,csrfmiddlewaretoken},
            success:function (result) {
                if(result['code'] == 200){
                    //获取博客id
                    let blog_id = result['data']['blog_id']
                    //跳转到博客详情界面
                    window.location = '/blog/detail/' + blog_id
                }else {
                    alert(result['message'])
                }
            }
        })
    })
}
