function getCtx(canvasId){
        var canvas = document.getElementById(canvasId);
        if(!canvas.getContext){
            alert('not support canvas');
            return;
        }
        var ctx = canvas.getContext('2d');
        return ctx;
        }
        
    //绘制折线图
    function draw(canvasId,unit){
        var strData = $('#'+canvasId).attr('data');
       
        var data = strData.split('');
        if(data.length==0){
            return ;
        }

        var canvas = document.getElementById(canvasId);
        if(!canvas.getContext){
            alert('not support canvas');
            return;
        }
        var ctx = canvas.getContext('2d');
         
        //ctx.moveTo(0,0);
        var x=0,y=0;
        for(var i in data){
            x = i * unit;
            y = (data.length-data[i])*unit; //?data.length - data[i]
            ctx.lineTo(x,y);
            //ctx.moveTo(x,y);
            console.log(x,y);
        }
        ctx.stroke();
    }

    function run(){
        $('canvas').each(function(){
          //  $(this).attr('id');
           // alert('?');
          // console.log($(this).attr('id'));
           var cId = $(this).attr('id');
            draw(cId,100/4); 
        })
    } 
    //draw('candle43512',100); 
    run();