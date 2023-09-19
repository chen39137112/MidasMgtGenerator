NODE_HEADER = """*NODE    ; Nodes
; iNO, X, Y, Z\n"""

ELEMENT_HEADER = """*ELEMENT    ; Elements
; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB,                     ; Frame  Element
; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB, EXVAL, EXVAL2, bLMT ; Comp/Tens Truss
; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iSUB, iWID , LCAXIS    ; Planar Element
; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iN5, iN6, iN7, iN8     ; Solid  Element\n"""

ELASTIC_LINK_HEADER = """*ELASTICLINK    ; Elastic Link
; iNO, iNODE1, iNODE2, LINK, ANGLE, R_SDx, R_SDy, R_SDz, R_SRx, R_SRy, R_SRz, SDx, SDy, SDz, SRx, SRy, SRz ... 
;                      bSHEAR, DRy, DRz, GROUP                                                                  ; GEN
; iNO, iNODE1, iNODE2, LINK, ANGLE, bSHEAR, DRy, DRz, GROUP                                                     ; RIGID,SADDLE
; iNO, iNODE1, iNODE2, LINK, ANGLE, SDx, bSHEAR, DRy, DRz, GROUP                                                ; TENS,COMP
; iNO, iNODE1, iNODE2, LINK, ANGLE, DIR, FUNCTION, bSHEAR, DRENDI, GROUP                                        ; MULTI LINEAR\n"""