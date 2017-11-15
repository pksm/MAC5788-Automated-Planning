;; Initial state:
;; $ git init
;; $ touch foo & nano foo
;; $ git add foo
;; $ touch bar & nano bar
;; $ touch baz
;; $ rm bar

;; Goals:
;; `foo` file is removed from staging area
;; `bar` file is recorded in staging area but not committed
;; `baz` changes are committed

(define (problem p03)
  (:domain git)
  (:objects foo bar baz - file)
  (:init
   (staged foo)
   (deleted-in-workspace bar)
   (untracked baz)
   )
  (:goal
   (and
    (modified-in-workspace foo)
    (staged bar)
    (committed baz))
  )
)