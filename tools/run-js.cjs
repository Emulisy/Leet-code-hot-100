// Execute an unchanged LeetCode JavaScript solution in its own context.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function ListNode(val = 0, next = null) {
  this.val = val;
  this.next = next;
}

function TreeNode(val = 0, left = null, right = null) {
  this.val = val;
  this.left = left;
  this.right = right;
}

function fromList(values) {
  return values.reduceRight((next, val) => new ListNode(val, next), null);
}

function fromTree(values) {
  if (!values?.length || values[0] === null) return null;
  const root = new TreeNode(values[0]);
  const queue = [root];
  let next = 1;
  for (let i = 0; i < queue.length && next < values.length; i++) {
    for (const side of ['left', 'right']) {
      if (next < values.length && values[next] !== null) {
        queue[i][side] = new TreeNode(values[next]);
        queue.push(queue[i][side]);
      }
      next++;
    }
  }
  return root;
}

function convert(value, type) {
  if (type === 'ListNode') return fromList(value ?? []);
  if (type === 'TreeNode') return fromTree(value);
  if (type.endsWith('[]')) return value.map(x => convert(x, type.slice(0, -2)));
  return value;
}

function serialize(value, type) {
  if (type === 'ListNode') {
    const result = [];
    const seen = new Set();
    for (let node = value; node !== null; node = node.next) {
      if (!node || seen.has(node)) throw new Error('Invalid or cyclic linked-list output');
      seen.add(node);
      result.push(node.val);
    }
    return result;
  }
  if (type === 'TreeNode') {
    const result = [];
    const queue = [value];
    const seen = new Set();
    for (let i = 0; i < queue.length; i++) {
      const node = queue[i];
      if (node == null) { result.push(null); continue; }
      if (seen.has(node)) throw new Error('Cyclic tree output');
      seen.add(node);
      result.push(node.val);
      queue.push(node.left, node.right);
    }
    while (result.at(-1) === null) result.pop();
    return result;
  }
  if (type.endsWith('[]')) return value.map(x => serialize(x, type.slice(0, -2)));
  return value;
}

const configPath = path.resolve(process.argv[2]);
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const sourcePath = path.join(path.dirname(configPath), config.file);
const raw = fs.readFileSync(0, 'utf8').trim().split(/\r?\n/).filter(x => x.trim());
if (raw.length !== config.params.length) throw new Error('Incorrect number of input arguments');
const args = raw.map((line, i) => convert(JSON.parse(line), config.params[i].type));
const context = vm.createContext({ console, ListNode, TreeNode });
new vm.Script(fs.readFileSync(sourcePath, 'utf8'), { filename: sourcePath }).runInContext(context);
context.__localArgs = args;
const result = new vm.Script(`${config.method}(...__localArgs)`, {
  filename: 'local-invocation.js',
}).runInContext(context);
const hasOutputArg = Number.isInteger(config.output_arg);
const answer = hasOutputArg ? args[config.output_arg] : result;
const type = hasOutputArg ? config.params[config.output_arg].type : config.return_type;
const output = serialize(answer, type);
if (output === undefined || (typeof output === 'number' && !Number.isFinite(output))) {
  throw new Error('Solution returned undefined or a non-finite number');
}
console.log('\noutput:', JSON.stringify(output));
if (Number.isInteger(config.check_prefix)) {
  console.log('mutated:', JSON.stringify(args[config.check_prefix]));
}
