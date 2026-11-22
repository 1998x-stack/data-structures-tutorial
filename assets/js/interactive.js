"use strict";
(function(){
 const chooser=document.querySelector('[data-demo="choice"]');
 if(chooser){
  const select=chooser.querySelector("select"),output=chooser.querySelector("output");
  const choices={
   random:"若主要操作是按整数下标取第 i 项，数组可通过偏移量定位槽位；在随机存取模型下是 O(1)。",
   front:"若已持有链表头节点，只需改变少量指针即可在表头插入，O(1)；但按下标查找仍为 O(n)。",
   lookup:"若大量按唯一键查找，可考虑哈希表：合理哈希和负载假设下预期 O(1)，碰撞或极端输入可能退化。",
   ordered:"若需要同时保持键有序与范围查询，可考虑平衡搜索树，典型增删查 O(log n)。"
  };
  const update=()=>{output.textContent=choices[select.value];};
  select.addEventListener("change",update);update();
 }
 const growth=document.querySelector('[data-demo="growth"]');
 if(growth){
  const input=growth.querySelector("input"),out=growth.querySelector("output");
  const update=()=>{
   const n=Number(input.value);
   const model=`n = ${n}：常数 1；以 2 为底对数约 ${Math.ceil(Math.log2(n))}；线性 ${n}；平方 ${n*n}。这些是抽象的操作数量级，不是实测耗时。`;
   out.textContent=model;
  };
  input.addEventListener("input",update);update();
 }
 const range=document.querySelector('[data-demo="range"]');
 if(range){
  const a=[2,-1,4,3,-2,5],left=range.querySelector('[name="left"]'),right=range.querySelector('[name="right"]'),out=range.querySelector("output"),cells=[...range.querySelectorAll(".cell")];
  const update=()=>{
   let l=Number(left.value),r=Number(right.value);
   if(l>r){r=l;right.value=String(r);}
   const p=[0];for(const x of a)p.push(p[p.length-1]+x);
   cells.forEach((cell,i)=>cell.classList.toggle("selected",i>=l&&i<r));
   out.textContent=`a[${l}:${r}] 的和 = P[${r}] − P[${l}] = ${p[r]} − ${p[l]} = ${p[r]-p[l]}。左闭右开；空区间和为 0。`;
  };
  left.addEventListener("input",update);right.addEventListener("input",update);update();
 }
})();