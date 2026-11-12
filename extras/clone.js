//shallow clone
function shallowClone(obj) {
    let newObj = {};
    for (let key in obj) {
        newObj[key] = obj[key];
    }
    return newObj;
}
// shallow clone is the same as:
function builtInShallowClone(obj) {
    return Object.assign({}, obj);
}

//deep clone recursion
function deepClone(value, seen = new WeakMap()) {
    // return if the value is not object or value is null
    if (typeof value !== "object" || value === null) return value;

    //deal with self reference
    if (seen.has(value)) return seen.get(value);

    //if value is Date
    if (value instanceof Date) return new Date(value);

    //RegExp
    if (value instanceof RegExp) return new RegExp(value.source, value.flags);

    //Map
    if (value instanceof Map) {
        const result = new Map();
        seen.set(value, result);
        for (const [k, v] of value.entries()) {
            result.set(deepClone(k, seen), deepClone(v, seen));
        }
        return result;
    }

    // 6) Set
    if (value instanceof Set) {
        const result = new Set();
        seen.set(value, result);
        for (const item of value.values()) {
            result.add(deepClone(item, seen));
        }
        return result;
    }

    // 7) Array / Object（保留原型）
    const result = Array.isArray(value)
        ? []
        : Object.create(Object.getPrototypeOf(value));

    seen.set(value, result);

    // 8) 拷贝所有 own keys（包含 Symbol）
    for (const key of Reflect.ownKeys(value)) {
        result[key] = deepClone(value[key], seen);
    }

    return result;
}


function myDeepClone(obj, seen = new WeakMap()) {
    // 1) 基本类型 或 null：直接返回
    if (typeof obj !== "object" || obj === null) return obj;

    // 2) 循环引用：直接返回缓存的克隆结果
    if (seen.has(obj)) return seen.get(obj);

    // 3) 创建新容器（数组/对象）
    const result = Array.isArray(obj) ? [] : {};

    // 4) 先缓存（关键：防止循环引用爆栈）
    seen.set(obj, result);

    // 5) 拷贝自己的 key（包含 Symbol）
    Object.getOwnPropertyNames(obj).forEach((key) => {
        result[key] = deepClone(obj[key], seen);
    })

    return result;
}

