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

 // Chapter 09: trace the comparison path of a BST search on a fixed tree.
 const bst=document.querySelector('[data-demo="bst-search"]');
 if(bst){
  const select=bst.querySelector("select"),out=bst.querySelector("output");
  const tree={v:5,l:{v:3,l:{v:2},r:{v:4}},r:{v:8,l:{v:7},r:{v:9}}};
  const update=()=>{
   const target=Number(select.value);
   const path=[];let node=tree,hit=false;
   while(node){path.push(node.v);if(target===node.v){hit=true;break;}node=target<node.v?node.l:node.r;}
   const trail=path.join(" → ")+(hit?"":" → 空");
   out.textContent="查找 "+target+"："+trail+"；"+(hit?"命中":"未找到")+"，比较 "+path.length+" 次。";
  };
  select.addEventListener("change",update);update();
 }

 // Chapter 10: describe the AVL fix for each of the four imbalance shapes.
 const avl=document.querySelector('[data-demo="avl-rotate"]');
 if(avl){
  const select=avl.querySelector("select"),out=avl.querySelector("output");
  const steps={
   LL:"插入 3,2,1：根 3 平衡因子 2，需 LL，对 3 右旋；结果根 2，中序 1,2,3。",
   RR:"插入 1,2,3：根 1 平衡因子 −2，需 RR，对 1 左旋；结果根 2，中序 1,2,3。",
   LR:"插入 3,1,2：根 3 平衡因子 2，左孩子 1 偏右，需 LR：先对 1 左旋，再对 3 右旋；结果根 2，中序 1,2,3。",
   RL:"插入 1,3,2：根 1 平衡因子 −2，右孩子 3 偏左，需 RL：先对 3 右旋，再对 1 左旋；结果根 2，中序 1,2,3。"
  };
  const update=()=>{out.textContent=steps[select.value];};
  select.addEventListener("change",update);update();
 }

 // Chapter 11: deterministic array states for a min-heap push/pop sequence.
 const heap=document.querySelector('[data-demo="heap-trace"]');
 if(heap){
  const input=heap.querySelector("input"),out=heap.querySelector("output");
  const states=[
   ["初始（空堆）","空","还没有元素。"],
   ["push(5)","[5]","空堆直接放入根。"],
   ["push(1)","[1, 5]","1 在末尾，小于父 5，上浮到根。"],
   ["push(3)","[1, 5, 3]","3 是 1 的孩子，父不大于子，无需交换。"],
   ["push(0)","[0, 1, 3, 5]","0 依次小于父 5 与父 1，上浮两步到根。"],
   ["pop() 返回 0","[1, 5, 3]","末尾 5 移到根，与较小的孩子 1 交换后恢复堆序。"]
  ];
  const update=()=>{const n=Number(input.value),s=states[n];out.textContent="第 "+n+" 步 "+s[0]+"：数组 "+s[1]+"。"+s[2];};
  input.addEventListener("input",update);update();
 }

 // Chapter 12: deterministic BFS layering on the figure's 0..4 graph.
 const bfs=document.querySelector('[data-demo="graph-bfs"]');
 if(bfs){
  const input=bfs.querySelector("input"),out=bfs.querySelector("output");
  const states=[
   ["初始","队列 [0]，已访问 {0}","0 入队，距离 0。"],
   ["第 1 层","队列 [1, 2]，已访问 {0,1,2}","从 0 找到邻居 1、2，距离都是 1。"],
   ["第 2 层","队列 [3]，已访问 {0,1,2,3}","1、2 都指向 3，3 第一次被访问，距离 2。"],
   ["第 3 层","队列 [4]，已访问 {0,1,2,3,4}","3 的邻居 4 距离 3，访问完毕。"]
  ];
  const update=()=>{const n=Number(input.value),s=states[n];out.textContent="第 "+n+" 步 "+s[0]+"："+s[1]+"。"+s[2];};
  input.addEventListener("input",update);update();
 }

 // Chapter 13: Dijkstra settling order on the figure's A..D graph.
 const dij=document.querySelector('[data-demo="dijkstra-trace"]');
 if(dij){
  const input=dij.querySelector("input"),out=dij.querySelector("output");
  const states=[
   ["初始","A=0，B=∞，C=∞，D=∞","只有起点距离已知。"],
   ["取出 A(0)","B=4，C=2","松弛 A 的两条出边。"],
   ["取出 C(2)","D=10","当前未定的顶点中 C 最近。"],
   ["取出 B(4)","D=9","经 B 到 D 是 4+5=9，比 10 更短。"],
   ["取出 D(9)","结束","已无出边，全部距离确定。"]
  ];
  const update=()=>{const n=Number(input.value),s=states[n];out.textContent="第 "+n+" 步 "+s[0]+"："+s[1]+"。"+s[2];};
  input.addEventListener("input",update);update();
 }

 // Chapter 14: deterministic insertion-sort states for a fixed array.
 const ins=document.querySelector('[data-demo="insertion-trace"]');
 if(ins){
  const input=ins.querySelector("input"),out=ins.querySelector("output");
  const states=[
   ["初始","[5, 2, 4, 6, 1, 3]","尚未开始，第一个元素视为已有序。"],
   ["i = 1","[2, 5, 4, 6, 1, 3]","插入 2：2 小于 5，前移一位。"],
   ["i = 2","[2, 4, 5, 6, 1, 3]","插入 4：4 落在 2 与 5 之间。"],
   ["i = 3","[2, 4, 5, 6, 1, 3]","插入 6：已大于左侧全部，不移动。"],
   ["i = 4","[1, 2, 4, 5, 6, 3]","插入 1：1 最小，前移到首位。"],
   ["i = 5","[1, 2, 3, 4, 5, 6]","插入 3：落到 2 与 4 之间，完成。"]
  ];
  const update=()=>{const n=Number(input.value),s=states[n];out.textContent=s[0]+"：数组 "+s[1]+"。"+s[2];};
  input.addEventListener("input",update);update();
 }

 // Chapter 15: lower_bound interval shrinking on a fixed sorted array.
 const bis=document.querySelector('[data-demo="bisect-trace"]');
 if(bis){
  const select=bis.querySelector("select"),out=bis.querySelector("output");
  const a=[1,3,3,5,7,9];
  const update=()=>{
   const target=Number(select.value);
   let lo=0,hi=a.length;const steps=[];
   while(lo<hi){const mid=lo+((hi-lo)>>1);steps.push(`[${lo},${hi}) 取 mid=${mid}（值 ${a[mid]}）`);if(a[mid]<target)lo=mid+1;else hi=mid;}
   out.textContent="查找 "+target+"："+steps.join(" → ")+"；最终插入位置为 "+lo+"（下标 "+lo+" 起均 ≥ "+target+"）。";
  };
  select.addEventListener("change",update);update();
 }

 // Chapter 15: naive vs memoized Fibonacci call counts on a fixed table.
 const fib=document.querySelector('[data-demo="fib-calls"]');
 if(fib){
  const input=fib.querySelector("input"),out=fib.querySelector("output");
  const calls=[1,1,3,5,9,15,25,41,67,109,177];
  const update=()=>{const n=Number(input.value);out.textContent="n = "+n+"：朴素递归共 "+calls[n]+" 次调用；记忆化只需计算 "+(n+1)+" 个不同的子问题。";};
  input.addEventListener("input",update);update();
 }

 // Chapter 16: DFS output order of permute([1,2,3]).
 const perm=document.querySelector('[data-demo="permute-order"]');
 if(perm){
  const input=perm.querySelector("input"),out=perm.querySelector("output");
  const perms=[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]];
  const update=()=>{const n=Number(input.value);out.textContent="第 "+(n+1)+" 个排列是 "+JSON.stringify(perms[n])+"（共 6 个；先序 DFS 的顺序）。";};
  input.addEventListener("input",update);update();
 }

 // Chapter 16: known N-queens solution counts.
 const qn=document.querySelector('[data-demo="queens-count"]');
 if(qn){
  const input=qn.querySelector("input"),out=qn.querySelector("output");
  const counts={1:1,2:0,3:0,4:2,5:10,6:4,7:40,8:92};
  const update=()=>{const n=Number(input.value);out.textContent="n = "+n+"：共有 "+counts[n]+" 个解。";};
  input.addEventListener("input",update);update();
 }

 // Chapter 17: rolling DP values for the house-robber example.
 const rob=document.querySelector('[data-demo="rob-trace"]');
 if(rob){
  const input=rob.querySelector("input"),out=rob.querySelector("output");
  const nums=[2,1,1,2];
  const vals=[2,2,3,4];
  const why=["偷第 1 间得 2。","第 2 间得 1，不如沿用 2。","偷第 1、3 间：2+1=3。","偷第 1、4 间：2+2=4，跳过中间两间。"];
  const update=()=>{const i=Number(input.value);out.textContent="处理到第 "+(i+1)+" 间（金额 "+nums[i]+"）：当前最优 dp = "+vals[i]+"。"+why[i];};
  input.addEventListener("input",update);update();
 }

 // Chapter 18: jump-game farthest reach after each index.
 const jr=document.querySelector('[data-demo="jump-reach"]');
 if(jr){
  const input=jr.querySelector("input"),out=jr.querySelector("output");
  const nums=[2,3,1,1,4];
  const reach=[2,4,4,4,8];
  const update=()=>{const i=Number(input.value);const done=reach[i]>=nums.length-1;out.textContent="处理 i="+i+"（可跳 "+nums[i]+"）：reach = "+reach[i]+(done?"，已覆盖终点下标 4。":"，尚未到达终点。");};
  input.addEventListener("input",update);update();
 }

 // Chapter 19: parent array after each union (path compression + rank).
 const uf=document.querySelector('[data-demo="uf-trace"]');
 if(uf){
  const input=uf.querySelector("input"),out=uf.querySelector("output");
  const steps=[
   ["初始",[0,1,2,3,4],5],
   ["union(0,1)",[0,0,2,3,4],4],
   ["union(2,3)",[0,0,2,2,4],3],
   ["union(1,2)",[0,0,0,2,4],2]
  ];
  const update=()=>{const n=Number(input.value),s=steps[n];out.textContent=s[0]+"：parent = ["+s[1].join(", ")+"]；当前集合数 = "+s[2]+"。";};
  input.addEventListener("input",update);update();
 }

 // Chapter 20: canonical segment-tree nodes covering a query range.
 const seg=document.querySelector('[data-demo="seg-query"]');
 if(seg){
  const a=[1,3,5,7,9,11,13,15],left=seg.querySelector('[name="l"]'),right=seg.querySelector('[name="r"]'),out=seg.querySelector("output");
  const collect=(node,lo,hi,l,r,acc)=>{
   if(r<lo||hi<l)return;
   if(l<=lo&&hi<=r){acc.push([lo,hi]);return;}
   const mid=(lo+hi)>>1;
   collect(2*node+1,lo,mid,l,r,acc);collect(2*node+2,mid+1,hi,l,r,acc);
  };
  const update=()=>{
   let l=Number(left.value),r=Number(right.value);
   if(l>r){r=l;right.value=String(r);}
   const acc=[];collect(0,0,a.length-1,l,r,acc);
   const parts=acc.map(([lo,hi])=>"sum["+lo+".."+hi+"]");
   const sum=acc.reduce((s,[lo,hi])=>{let t=0;for(let i=lo;i<=hi;i++)t+=a[i];return s+t;},0);
   out.textContent="查询 ["+l+", "+r+"]：覆盖 "+parts.join(" + ")+" = "+sum+"。共 "+parts.length+" 个节点（每层最多 2 个）。";
  };
  left.addEventListener("input",update);right.addEventListener("input",update);update();
 }

 // Chapter 21: autocomplete results for a fixed word list.
 const trieDemo=document.querySelector('[data-demo="trie-complete"]');
 if(trieDemo){
  const select=trieDemo.querySelector("select"),out=trieDemo.querySelector("output");
  const results={
   ap:["app","apple","apply","application","apt"],
   app:["app","apple","apply","application"],
   appl:["apple","apply","application"],
   b:["bat"],
   z:[]
  };
  const update=()=>{const key=select.value,list=results[key];out.textContent="前缀 "+key+"："+(list.length?list.join(", "):"没有匹配的词")+"（共 "+list.length+" 个）。";};
  select.addEventListener("change",update);update();
 }

 // Chapter 22: search walk on the documented skip list.
 const skip=document.querySelector('[data-demo="skip-search"]');
 if(skip){
  const select=skip.querySelector("select"),out=skip.querySelector("output");
  const paths={
   11:"L2 从 1 走到 7（下一位 13 超过）→ 降到 L1，从 7 走到 9 → 降到 L0，9 之后是 11，命中。",
   7:"L2 从 1 直接走到 7，命中（7 在最高层就存在）。",
   4:"L2 1 → 7（超过）降层；L1 1 → 3（下一位 7 超过）降层；L0 3 之后是 5，越过 4，未找到。",
   13:"L2 从 1 走到 7，再走到 13，命中。"
  };
  const update=()=>{out.textContent="查找 "+select.value+"："+paths[select.value];};
  select.addEventListener("change",update);update();
 }

 // Chapter 26: branch-transition model for sorted vs shuffled data.
 const branch=document.querySelector('[data-demo="branch-pattern"]');
 if(branch){
  const select=branch.querySelector("select"),out=branch.querySelector("output");
  const n=256,T=128;
  const sorted=[...Array(n).keys()];
  const rnd=[...Array(n).keys()];
  let seed=12345;
  const next=()=>{seed=(seed*1103515245+12345)&0x7fffffff;return seed;};
  for(let i=n-1;i>0;i--){const j=next()%(i+1);const t=rnd[i];rnd[i]=rnd[j];rnd[j]=t;}
  const transitions=a=>{let c=0;for(let i=1;i<a.length;i++){if((a[i]<T)!==(a[i-1]<T))c++;}return c;};
  const update=()=>{
   const data=select.value==="sorted"?sorted:rnd;
   out.textContent=(select.value==="sorted"?"有序":"乱序")+"数据：跳变 "+transitions(data)+" 次（共 "+(n-1)+" 个相邻对）；跳变越多，分支越难预测。";
  };
  select.addEventListener("change",update);update();
 }

 // Chapter 27: learned-index prediction window (teaching model).
 const li=document.querySelector('[data-demo="learned-pos"]');
 if(li){
  const select=li.querySelector("select"),out=li.querySelector("output");
  const keys=[1,3,5,7,9,11,13,15],window=4;
  const predict=k=>{const n=keys.length,lo=keys[0],hi=keys[n-1];let r=(k-lo)/(hi-lo);r=Math.min(1,Math.max(0,r));return Math.floor(r*(n-1));};
  const update=()=>{
   const key=Number(select.value),pos=predict(key);
   const lo=Math.max(0,pos-window),hi=Math.min(keys.length-1,pos+window);
   let a=lo,b=hi,found=-1;
   while(a<=b){const mid=(a+b)>>1;if(keys[mid]===key){found=mid;break;}if(keys[mid]<key)a=mid+1;else b=mid-1;}
   out.textContent="key="+key+"：预测位置 "+pos+"；窗口 ["+lo+", "+hi+"]；在窗口内二分，"+(found>=0?("找到它位于下标 "+found+"。"):"未找到（该 key 不在数组中）。");
  };
  select.addEventListener("change",update);update();
 }

 // Chapter 25: sliding-window rate limiter walkthrough.
 const rl=document.querySelector('[data-demo="rate-limit"]');
 if(rl){
  const input=rl.querySelector("input"),out=rl.querySelector("output");
  const times=[0,200,400,600,800,1000,1200,1400],limit=4,window=1000;
  const events=[]; const q=[];
  for(const t of times){
   while(q.length && q[0]<=t-window) q.shift();
   const allowed=q.length<limit;
   if(allowed) q.push(t);
   events.push({t,allowed,queue:[...q]});
  }
  const fmt=a=>a.join(", ");
  const update=()=>{
   const k=Number(input.value);
   if(k===0){out.textContent="处理前：窗口为空。";return;}
   const e=events[k-1];
   out.textContent="请求 "+e.t+"ms："+(e.allowed?"允许":"拒绝")+"；窗口内 "+e.queue.length+" 个（"+fmt(e.queue)+"）。";
  };
  input.addEventListener("input",update);update();
 }

 // Chapter 23: spaced-review schedule for the notebook.
 const rp=document.querySelector('[data-demo="review-plan"]');
 if(rp){
  const input=rp.querySelector("input"),out=rp.querySelector("output");
  const intervals=[1,3,7,30];
  const update=()=>{
   let start=Number(input.value);
   if(!Number.isFinite(start)||start<0) start=0;
   const days=intervals.map(d=>start+d);
   out.textContent="第 0 天 = "+start+"：复习日为 "+days.join("、")+"。";
  };
  input.addEventListener("input",update);update();
 }

})();