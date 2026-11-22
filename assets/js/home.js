"use strict";
const input=document.querySelector("#chapter-search");
const cards=[...document.querySelectorAll(".chapter-card")];
const status=document.querySelector("#search-status");
input?.addEventListener("input",()=>{
 const q=input.value.trim().toLocaleLowerCase("zh-CN");let shown=0;
 for(const card of cards){card.hidden=!card.dataset.search.includes(q);if(!card.hidden)shown++;}
 for(const section of document.querySelectorAll(".module")){section.hidden=![...section.querySelectorAll(".chapter-card")].some(card=>!card.hidden);}
 document.querySelector("#empty-state").hidden=shown!==0;
 status.textContent="显示 "+shown+" / "+cards.length+" 章";
});