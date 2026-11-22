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


 // Chapter 04: trace pointer rewiring using a fixed three-node example.
 const reverse=document.querySelector('[data-demo="reverse-links"]');
 if(reverse){
  const input=reverse.querySelector("input"),out=reverse.querySelector("output");
  const states=[
   "第 0 步：prev = None；cur = A → B → C；尚未修改链接。",
   "第 1 步：prev = A → None；cur = B → C；已处理 1 个节点。",
   "第 2 步：prev = B → A → None；cur = C；已处理 2 个节点。",
   "第 3 步：prev = C → B → A → None；cur = None；反转结束。"
  ];
  const update=()=>{out.textContent=states[Number(input.value)];};
  input.addEventListener("input",update);update();
 }

 // Chapter 05: view valid nested brackets under a prefix scan.
 const bracket=document.querySelector('[data-demo="bracket-trace"]');
 if(bracket){
  const input=bracket.querySelector("input"),out=bracket.querySelector("output");
  const steps=["空","{","{ [","{ [ (","{ [","{","空"];
  const update=()=>{const n=Number(input.value);out.textContent="读入前 "+n+" 个字符，栈自底向顶："+steps[n]+"。";};
  input.addEventListener("input",update);update();
 }

 // Chapter 06: exact queue states for the documented sequence.
 const ring=document.querySelector('[data-demo="ring-queue"]');
 if(ring){
  const input=ring.querySelector("input"),out=ring.querySelector("output");
  const states=[
   ["初始空队列","空",0,0,0],
   ["入队 A","A",0,1,1],
   ["入队 B","A,B",0,2,2],
   ["入队 C","A,B,C",0,3,3],
   ["出队 A","B,C",1,3,2],
   ["入队 D","B,C,D",1,0,3],
   ["入队 E","B,C,D,E",1,1,4]
  ];
  const update=()=>{const n=Number(input.value),s=states[n];out.textContent="第 "+n+" 步："+s[0]+"；队列 "+s[1]+"；front="+s[2]+"，rear="+s[3]+"，size="+s[4]+"。"+(n===5||n===6?" 队尾已经绕回索引 0。":"");};
  input.addEventListener("input",update);update();
 }

 // Chapter 07: deterministic toy hash, not CPython's hash layout.
 const hash=document.querySelector('[data-demo="hash-bucket"]');
 if(hash){
  const select=hash.querySelector("select"),out=hash.querySelector("output");
  const keys=[12,17,22,8];
  const update=()=>{
   const key=Number(select.value),bucket=key%5;
   const others=keys.filter(x=>x!==key && x%5===bucket);
   out.textContent="键 "+key+" → 桶 "+bucket+"；"+(others.length?"桶中还有 "+others.join("、")+"，必须比较完整键。":"目前没有其他示例键与它碰撞。");
  };
  select.addEventListener("change",update);update();
 }

 // Chapter 08: derive traversal orders from tree links rather than mere labels.
 const traversal=document.querySelector('[data-demo="tree-traversal"]');
 if(traversal){
  const select=traversal.querySelector("select"),out=traversal.querySelector("output");
  const root={v:4,l:{v:2,l:{v:1},r:{v:3}},r:{v:6,l:{v:5}}};
  const dfs=(n,mode,result)=>{
   if(!n)return;
   if(mode==="pre")result.push(n.v);
   dfs(n.l,mode,result);
   if(mode==="in")result.push(n.v);
   dfs(n.r,mode,result);
   if(mode==="post")result.push(n.v);
  };
  const labels={pre:"前序",in:"中序",post:"后序",level:"层序"};
  const update=()=>{
   const mode=select.value,result=[];
   if(mode==="level"){
    const queue=[root];
    for(let i=0;i<queue.length;i++){const n=queue[i];result.push(n.v);if(n.l)queue.push(n.l);if(n.r)queue.push(n.r);}
   } else dfs(root,mode,result);
   out.textContent=labels[mode]+"访问顺序："+result.join(" → ")+"。";
  };
  select.addEventListener("change",update);update();
 }

})();