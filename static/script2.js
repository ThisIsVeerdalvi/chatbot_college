class ChatBox{
    constructor(){
        this.args={
            onSend:document.querySelector('.SendBut'),
            chatBox:document.querySelector('#chat-box')
        };
        this.state=false;
        this.messages=[]; // to store the messsage in the list
        this.currentmsg='';
    }
    display(){
        const {onSend,chatBox}=this.args;
        onSend.addEventListener('click',()=>this.onSendFun(chatBox));

        let ketTag=document.querySelector("#chat-input");
        ketTag.addEventListener('keyup',({key})=>{
            if(key==='Enter'){
                window.alert("keyPressed");
            }
        })
    }
    onSendFun(chatbox){
        let tF=document.querySelector('#chat-input');

        let m1=tF.value;

        // if user is not entered any text then return the function 
        if(m1===''){
            return;
        }
        let msg1={name:"You",message:m1}
        this.messages.push(msg1)
        fetch('http://127.0.0.1:5000/predict',{
            method:'POST',
            body:JSON.stringify({message:m1}),
            mode:'cors',
            headers:{'Content-Type':'application/json'}
        })
        .then(respond=>respond.json())
        .then(respond=>{
            let msg2={name:'siri',message:respond.answer};
            console.log(respond.answer);
            this.messages.push(msg2);
            this.currentmsg=msg2;
            this.updateChat(chatbox);
            tF.value=""; // reset the value to null after click on send button
            this.SpeakMsg();
        })
        .catch((error)=>{
            console.log("Something error is occured");
            this.updateChat(chatbox)
            tF.value='';
        })

    }
        updateChat(chatbox){
            let html='';
                this.messages.slice().forEach(function(item,index){
                    if(item.name==='siri'){
                            html+='<div class="bot-chat"><p>'+item.message+'</p></div>';
                    }
                    else{
                        html+='<div class="my-chat"><p>'+item.message+'</p></div>';
                    }
                })

                let Ucode=chatbox.querySelector(".chat-msg");
                Ucode.innerHTML=html;
        }
        SpeakMsg(){
            let obj=new SpeechSynthesisUtterance();
            obj.text=this.currentmsg;
            window.speechSynthesis.speak(obj);
        }
}

let object=new ChatBox();
object.display();

