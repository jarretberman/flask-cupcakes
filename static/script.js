$(document).ready(()=>{
    $('form').on('submit', async(evt)=>{
        evt.preventDefault()
        const obj = {
            flavor : $('#flavor').val(),
            rating : $('#rating').val(),
            size : $('#size').val(),
            image : $('#image').val()
        }
        try{
        const res = await axios.post('/api/cupcakes', obj);
        } catch(e){
            alert('POST failed')
            console.log(e)
            return
        }
        const obj2 = res.data
        const $li = $('<li>')
        for (key in obj2){
            $li.append(`<p>${key} : ${obj2[key]}</p>`)
        }
        $('ul').append($li)
    })

    $('#get').on('click', async function(evt){
        evt.preventDefault()
        $('#cupcakes').empty()
        const res = await axios.get('/api/cupcakes')
        console.log(res.data)
        for(cupcake of res.data.cupcakes){
            const $li = $('<li>')
            for (key in cupcake){
                $li.append(`<p>${key} : ${cupcake[key]}</p>`)
            }
            $('ul').append($li)
        }


    })
})