; Domain - GitPlanner
; -----------------------------------------------------------------------
; Paula Kintschev S. de Moraes
; Numero USP: 10380758
; ------------------------------------------------------------------------

(define (domain git)

    (:requirements :strips :typing )

    (:types file)

    (:predicates
        (untracked ?f - file)
        (staged ?f - file)
        (committed ?f - file)
        (clean ?f - file)
        (modified-in-workspace ?f - file)
        (deleted-in-workspace ?f - file)
    )

    (:action git-add-new
        :parameters (?f - file)
        :precondition (and 
            (untracked ?f)
        )
        :effect (and 
            (not (untracked ?f)) 
            (staged ?f) 
            (clean ?f)
        )
    )

    (:action git-add
        :parameters (?f - file)
        :precondition (and 
            (modified-in-workspace ?f)
        )
        :effect (and 
            (staged ?f)
            (not(modified-in-workspace ?f))
        )
    )
    
    ;; git rm <old-file>
    (:action git-rm
        :parameters (?f - file)
        :precondition (and 
            (deleted-in-workspace ?f)
        )
        :effect (and 
            (untracked ?f) 
            (not(deleted-in-workspace ?f))
        )
    )

    (:action git-checkout
        :parameters (?f - file)
        :precondition (and 
            (modified-in-workspace ?f)
        )
        :effect (and 
            (clean ?f) 
            (not (modified-in-workspace ?f))
        )
    )

    (:action git-reset
        :parameters (?f - file)
        :precondition (and 
            (clean ?f)
        )
        :effect (and 
            (not (clean ?f)) 
            (modified-in-workspace ?f) 
        )
    )

    (:action git-reset-new
        :parameters (?f - file)
        :precondition (and 
            (staged ?f)
        )
        :effect (and 
            (deleted-in-workspace ?f)
            (not(staged ?f))
        )
    )

    (:action git-commit
        :parameters (?f - file)
        :precondition (and 
            (staged ?f)
        )
        :effect (and 
            (committed ?f) 
            (not (staged ?f)) 
            (clean ?f)
        )
    )
)
