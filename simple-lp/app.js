'use strict';
const jobs=[
 {id:'sample-01',title:'学びを実務の一歩へ。経理アシスタント',company:'事業会社の募集例',category:'簿記',salary:'年収 320〜450万円',location:'東京都・一部在宅',tags:['簿記2級を活かす','未経験から相談可'],description:'仕訳入力や経費精算、請求書の確認など、日々の経理業務をチームで担当する仕事の例です。',requirement:'簿記2級の知識を持つ方を想定。実務経験の要否は、正式な募集条件で確認します。',support:'入社後の業務指導や学習支援制度のある募集を想定しています。'},
 {id:'sample-02',title:'科目合格を次のステップに。税務会計スタッフ',company:'税理士事務所の募集例',category:'税理士',salary:'年収 350〜550万円',location:'大阪府・正社員',tags:['科目合格を活かす','試験との両立'],description:'会計データの整理、決算や税務申告の補助などを担当する仕事の例です。資格学習と実務の接点を考えるためのサンプルです。',requirement:'税理士試験の科目合格や会計事務所での経験を活かす想定です。担当可能な業務範囲は正式募集時に確認します。',support:'試験前休暇や通学との両立に配慮した募集を想定しています。'},
 {id:'sample-03',title:'資格と対話力を活かす、不動産の契約サポート',company:'不動産会社の募集例',category:'宅建',salary:'年収 350〜500万円',location:'神奈川県・正社員',tags:['宅建資格を活かす','営業経験も活きる'],description:'不動産契約に関する書類の確認や、お客様へのご案内を行う仕事の例です。',requirement:'宅地建物取引士資格を持つ方を想定。登録・証の交付状況と担当業務は正式募集時に確認します。',support:'業務に必要な知識をチームで学び、経験を広げる募集を想定しています。'},
 {id:'sample-04',title:'人と組織を支える、人事・労務アシスタント',company:'事業会社の募集例',category:'社労士',salary:'年収 330〜480万円',location:'東京都・一部在宅',tags:['社労士の学びを活かす','学習中から相談可'],description:'勤怠の確認や給与計算の補助、社内の労務手続きなどを担当する仕事の例です。',requirement:'人事労務への関心と基礎知識を持つ方を想定。社労士資格や実務経験の必要性は募集ごとに確認します。',support:'実務の基礎から役割を広げる募集を想定しています。'},
 {id:'sample-05',title:'会計の基礎から専門性を磨く、会計事務所スタッフ',company:'会計事務所の募集例',category:'簿記',salary:'年収 300〜420万円',location:'愛知県・正社員',tags:['簿記を学習中の方も','段階的に業務を習得'],description:'帳簿の入力や証憑の整理から、経験に応じて月次業務などに携わる仕事の例です。',requirement:'簿記の学習経験がある方を想定。資格取得前に応募できるかは、実際の募集要件を確認します。',support:'学習と仕事の両立を相談できる募集を想定しています。'},
 {id:'sample-06',title:'経験と資格を組み合わせる、税務会計の次のキャリア',company:'税理士法人の募集例',category:'税理士',salary:'年収 450〜650万円',location:'首都圏・正社員',tags:['会計経験を活かす','専門性を広げる'],description:'会計や税務の実務経験を活かしながら、お客様の課題に向き合う仕事の例です。',requirement:'会計・税務の実務経験や科目合格を想定。必要な経験年数や資格は正式な募集条件で確認します。',support:'専門知識の向上や、担当領域の拡大を支援する募集を想定しています。'}
];
const grid=document.querySelector('#job-grid');
const symbols={'簿記':'帳','税理士':'税','宅建':'住','社労士':'人'};
function renderJobs(category='all'){
 const shown=jobs.filter(job=>category==='all'||job.category===category);
 grid.innerHTML=shown.map(job=>`<article class="job-card"><div class="job-card-top"><span class="job-symbol" aria-hidden="true">${symbols[job.category]}</span><span class="sample-label">SAMPLE JOB</span></div><p class="company">${job.company}</p><h3>${job.title}</h3><dl class="job-meta"><div><dt>給与</dt><dd>${job.salary}</dd></div><div><dt>勤務地</dt><dd>${job.location}</dd></div></dl><div class="tags">${job.tags.map((tag,i)=>`<span class="tag ${i===0?'orange':''}">${tag}</span>`).join('')}</div><button class="card-detail" data-job="${job.id}">求人の詳細を見る <span aria-hidden="true">↗</span></button></article>`).join('');
 document.querySelector('.job-count').textContent=`${shown.length}件のサンプル`;
}
renderJobs();
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
 document.querySelectorAll('[data-filter]').forEach(x=>{x.classList.toggle('active',x===button);x.setAttribute('aria-pressed',String(x===button));});renderJobs(button.dataset.filter);
}));
const jobDialog=document.querySelector('#job-dialog');let currentJob=null;let selectedJob=null;
grid.addEventListener('click',event=>{
 const button=event.target.closest('[data-job]');if(!button)return;
 currentJob=jobs.find(job=>job.id===button.dataset.job);
 const job=currentJob;
 document.querySelector('#job-detail').innerHTML=`<p class="dialog-company">${job.company}</p><h2 id="job-dialog-title">${job.title}</h2><dl class="detail-table"><div><dt>給与例</dt><dd>${job.salary}</dd></div><div><dt>勤務地例</dt><dd>${job.location}</dd></div><div><dt>関連する資格</dt><dd>${job.category}</dd></div></dl><h3>仕事内容のイメージ</h3><p>${job.description}</p><h3>応募条件のイメージ</h3><p>${job.requirement}</p><h3>学習・キャリア支援のイメージ</h3><p>${job.support}</p><p class="dialog-notice">この求人は架空のサンプルです。実際の企業・募集・給与・制度を示すものではなく、応募もできません。</p>`;
 jobDialog.showModal();
});
document.querySelector('#job-register').addEventListener('click',()=>{
 selectedJob=currentJob;document.querySelector('#selected-job-title').textContent=selectedJob.title;document.querySelector('#selected-job').hidden=false;
 document.querySelector('input[name="purpose"][value="求人紹介"]').checked=true;
 jobDialog.close();document.querySelector('#register').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
});
document.querySelector('#clear-job').addEventListener('click',()=>{selectedJob=null;document.querySelector('#selected-job').hidden=true;document.querySelector('#selected-job-title').textContent='';});
document.querySelectorAll('dialog').forEach(dialog=>{
 dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
 dialog.querySelectorAll('.close-dialog').forEach(button=>button.addEventListener('click',()=>dialog.close()));
});
const policyCopy={
 terms:{title:'利用条件について',body:'このページはスタディングキャリアのサービス構想を確認するための試作版です。実際の会員登録・求人応募・人材紹介の申込みは受け付けていません。正式公開前に、運営主体、支援範囲、登録条件、連絡方法、退会方法などを定めた利用条件を掲載します。'},
 privacy:{title:'入力情報の取扱いについて',body:'入力内容は、このページを開いている間の画面表示にのみ使われます。登録データをサーバーへ送信せず、ブラウザの保存領域にも保存しません。ページを閉じる、または再読み込みすると入力内容は失われます。実際の個人情報を入力せず、サンプル情報でお試しください。正式な受付を始める際は、利用目的、提供先、保存・削除、問い合わせ先を含む説明を別途掲載します。'},
 company:{title:'運営について',body:'スタディングキャリアはKIYOラーニング株式会社が運営するサービスです。このページは既存サービスの調査資料を参考に作成した、再構築に向けた非公開の試作版です。正式な問い合わせ窓口と事業情報は、公開時に確認して掲載します。'}
};
document.querySelectorAll('[data-policy]').forEach(button=>button.addEventListener('click',()=>{
 const copy=policyCopy[button.dataset.policy];document.querySelector('#info-title').textContent=copy.title;document.querySelector('#info-body').textContent=copy.body;document.querySelector('#info-dialog').showModal();
}));
const form=document.querySelector('#registration');const confirmation=document.querySelector('#confirmation');
function addRow(parent,label,value){const row=document.createElement('div');const dt=document.createElement('dt');const dd=document.createElement('dd');dt.textContent=label;dd.textContent=value;row.append(dt,dd);parent.append(row);}
form.addEventListener('submit',event=>{
 event.preventDefault();const error=document.querySelector('#form-error');error.textContent='';
 const name=document.querySelector('#name');const email=document.querySelector('#email');
 const qualifications=[...form.querySelectorAll('[name="qualification"]:checked')].map(x=>x.value);
 if(!name.value.trim()){error.textContent='お名前を入力してください。';name.focus();return;}
 if(!email.value.trim()||!email.validity.valid){error.textContent='メールアドレスを正しい形式で入力してください。';email.focus();return;}
 if(!qualifications.length){error.textContent='資格を一つ以上選択してください。検討中の方は「その他・検討中」を選べます。';form.querySelector('[name="qualification"]').focus();return;}
 const purpose=form.querySelector('[name="purpose"]:checked');
 if(!purpose){error.textContent='登録後のご希望を選択してください。';form.querySelector('[name="purpose"]').focus();return;}
 if(!document.querySelector('#consent').checked){error.textContent='利用条件・個人情報の取扱いの説明をご確認ください。';document.querySelector('#consent').focus();return;}
 const rows=document.querySelector('#confirmation-data');rows.replaceChildren();
 [['お名前',name.value.trim()],['メール',email.value.trim()],['資格',qualifications.join('、')],['勤務エリア',document.querySelector('#location').value||'未選択'],['ご希望',purpose.parentElement.textContent.trim()],['気になる求人',selectedJob?selectedJob.title:'未選択'],['伝えたいこと',document.querySelector('#message').value.trim()||'なし']].forEach(([label,value])=>addRow(rows,label,value));
 confirmation.showModal();
});
document.querySelector('#finish-demo').addEventListener('click',()=>{
 confirmation.close();form.reset();selectedJob=null;document.querySelector('#selected-job').hidden=true;document.querySelector('#selected-job-title').textContent='';document.querySelector('#confirmation-data').replaceChildren();
 document.querySelector('#info-title').textContent='登録の体験が完了しました。';document.querySelector('#info-body').textContent='入力内容は送信・保存されていません。画面上の入力情報も消去しました。正式公開時は、メール認証と受付の仕組みを接続します。';document.querySelector('#info-dialog').showModal();
});
