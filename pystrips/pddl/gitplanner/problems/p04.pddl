;; Initial state:
;; $ git init
;; $ touch foo & nano foo
;; $ git add foo
;; $ git commit foo
;; $ nano foo
;; $ touch bar & nano bar
;; $ git add bar
;; $ git commit bar
;; $ rm bar
;; $ touch baz & nano baz
;; $ git add baz
;; $ git commit baz
;; $ git nano baz

;; Goals:
;; `baz` changes are erased (back to committed state)
;; `bar` changes are committed
;; `foo` changes are committed

(define (problem p04)
  (:domain git)
  (:objects foo bar baz - file)
  (:init
   (modified-in-workspace foo)
   (deleted-in-workspace bar)
   (modified-in-workspace baz)
   )
  (:goal
   (and
    (committed bar)
    (committed foo)
    (clean baz)
    )
  )
)
