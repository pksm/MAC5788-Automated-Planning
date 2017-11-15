;; Initial state:
;; $ git init
;; $ touch foo & nano foo
;; $ git add foo
;; $ touch bar

;; Goals:
;; Undo the `git add` operation so `foo` file remains untracked.
;; Add and commit `bar` file.

(define (problem p02)
  (:domain git)
  (:objects foo bar - file)
  (:init
   (staged foo)
   (untracked bar)
  )
  (:goal
   (and (untracked foo)
        (committed bar))
  )
)
