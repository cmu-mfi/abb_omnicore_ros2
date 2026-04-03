! Source: https://gitlab.cvh-server.de/jweber/abb_egm_driver/-/blob/master/abb_egm_driver/rapid/EGM_joint_trajectory.mod?ref_type=heads

MODULE TRob1Main
    PROC main()
        !TPWrite "Start EGM interface";

        ! Identifier for the EGM handler.
        VAR egmident egm_id;

        ! Limits for convergance.
        VAR egm_minmax cond_angle := [-0.1, 0.1]; ! degree

        ! Register an EGM id.
        EGMGetId egm_id;
        EGMSetupUC ROB_1, egm_id, "default", "ROB_1", \Joint, \CommTimeout:=5;

        ! Prepare for an EGM communication session.
        EGMActJoint egm_id
                \StreamStart
                \J1:=cond_angle
                \J2:=cond_angle
                \J3:=cond_angle
                \J4:=cond_angle
                \J5:=cond_angle
                \J6:=cond_angle
                \LpFilter:=15
                \SampleRate:=4
                \MaxSpeedDeviation:=25.0;
        WHILE TRUE DO
            ! Start the EGM communication session.
            EGMRunJoint egm_id, EGM_STOP_HOLD,\J1 \J2 \J3 \J4 \J5 \J6 \CondTime:=9999999;
        ENDWHILE

        ERROR
            TPWrite "Error!";
            IF ERRNO = ERR_UDPUC_COMM THEN
                TPWrite "Communication timedout";
                TRYNEXT;
            ENDIF
    ENDPROC
ENDMODULE
