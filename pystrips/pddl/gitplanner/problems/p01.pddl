;; Initial state:
;; $ git init
;; $ touch foo

;; Goal:
;; `foo` file committed.

(define (problem p01)
  (:domain git)
  (:objects foo - file)
  (:init
    (untracked foo)
  )
  (:goal
    (and (committed foo))
  )
)