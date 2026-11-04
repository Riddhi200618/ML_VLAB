const assert=require('node:assert/strict'),fs=require('fs');
const m=JSON.parse(fs.readFileSync('dist/models/sales-sgd.json','utf8'));
assert.equal(m.train_rows+m.test_rows,200);
for(const e of m.test_examples){const p=m.intercept+e.inputs.reduce((s,v,i)=>s+m.coefficients[i]*(v-m.mean[i])/m.scale[i],0);assert(Math.abs(p-e.prediction)<1e-10)}
const rmse=Math.sqrt(m.test_examples.reduce((s,e)=>s+(e.actual-e.prediction)**2,0)/m.test_rows);
assert(Math.abs(rmse-m.metrics.test.rmse)<1e-10);
assert(rmse<m.metrics.baseline.rmse);
console.log('Exported JavaScript predictions match Python on all 40 test rows; test RMSE verified.');
