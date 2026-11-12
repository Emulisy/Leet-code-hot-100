// var rotateRight = function(head, k) {
//     if (!head || !head.next || k === 0) return head;
//
//     function rotateOnce(head) {
//         let current = head;
//         while (current.next.next) {
//             current = current.next;
//         }
//         current.next.next = head;
//         head = current.next;
//         current.next = null;
//         return head;
//     }
//
//     for (let i = 1; i <= k; i++) {
//         head = rotateOnce(head);
//     }
//
//     return head;
// };

//exceed time limit

/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @param {number} k
 * @return {ListNode}
 */
var rotateRight = function(head, k) {
    if(!head || !head.next || k === 0) return head;

    let tail = head;
    let len = 1;

    while(tail.next) {
        tail = tail.next;
        len ++;
    }

    k = k % len;
    if (k === 0) return head;

    tail.next = head;

    let steps = len - k - 1;
    let current = head;
    while (steps > 0) {
        current = current.next;
        steps--;
    }

    let newHead = current.next;
    current.next = null;

    return newHead;
};
