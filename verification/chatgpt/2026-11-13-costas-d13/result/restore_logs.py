#!/usr/bin/env python3
"""Restore original byte-exact run logs from an embedded zlib+base85 text bundle."""
from pathlib import Path
import base64, hashlib, json, zlib
PAYLOAD = (
    "c-"
    "p<4ZEq&Gb%y_nut2}bGRbrJX22iZc#8(D6T^;y6fm$*ca?a%YiS{Ao4%m`y&Or;JTtm4%G%WFhqQ@(#AoK*9Fpf6&dvXRasKhm+u"
    "P4>em;Ny{_OqLpI?0O;_}OQ^7Z)7hpU^nw{QRb;??EVn~R$-)5)LC-@d<i^Xm5e`p*})5C1g$czHSg)z{-"
    "ckK%0}Z_kg<OT3SGe;l9Z?dRvmdriw<l<^nk@n858w@~R1VhZ>dHG8f<UcNYeadG+a=Zov}+lx)EUtfK^ydD4lkmj3<*H@Qs#_yb"
    "k5Ug8^?c`6R(Jx=0-=2>@`*?Bl`Rl8j+w+@v_OEX*?*+JTB%K`Yb=OGjZmmxmNry)4p%H&*B>KLUWF_U<rP!erKitpZTD-"
    "5#*jdPyE<Ou+(uyBi$%ktRhl}Z9Z6=+?*y|I`<U=#%a51qwv{T!o+*qle%A}!kXs8|%91a&`OD^{L$tio9v{Vl*wZonHG0&;jeN("
    "N+lzh@uJ2cfFnyTe+QN`WDt|^aRY?h~fXeoxn{l&E{3!XyUHkQ1V9%p?qtc@MIv|DNGJzCAX4i&AYGVR!F&yI(#J%l^-sM2e-"
    "vc0s@LuoS+<J!Zct(~)_!=;%ui^<xim$shUOvw1q)5pVnb8&wC`lrt>V|+I*czvMb$-BE89RBh?53kQJuP)!dK7aq}`s(U-"
    "Jfb<D-2QZZasKB1alQTc;ngNP<9^(Ky!`t2zk7MI{K1z8Sw<(b<u-o)@c!cV;?0-"
    "w^U=~a@Gy{+=%H=`)8oKH|7*Sawncj!Xa^BP?_M^M{y1`#J9@UZiOi29%dt%hX%kuGe%3*4^hn=CR*8(8$6)*GO(GBX-"
    "o3YNWS7Xp&9_=CZu1@_G#^I1*1|STQ8lWE;V8Dcz56ICts_^A!F$-oicoRQe+p*1Sdl9B!;Pid`!-"
    "axO6!9c#;CUq6|vGmf*RtkQ$<lLt=%e)hk2J;(JQUffJIB&UL8fTw2rG`OuO65O(NMk2(-"
    "}hwr?eoEcK%fmbaIiM6;Av9a;&ySbeyTopubq+fb3r)+sfNd2|~plG!0)eLP>g3lPcdphNDl>;?>x%-"
    "X7M+I7VwirGPh>Z6ZuLq#ylYpcz-p(c9S;bADF&u%-"
    "diC)&%+sb7tt?59xPI*1WU8}0r;lb^>hFz<omZx>eQTG=hYWbRhX1>j<iCV{1LyB$pB$&wM$AR0d?qWqRU(@BbduUAb^5fWDmZis"
    "LJ`lmYu20QaOl;eAQOw(#+mYREs3?}#QF%<0yBSFo%Xxji#;mjr6~*#8$^<vxU93o!eO-"
    ")<HRLu_B+JM9ihcVmx+s<psqHoGFF*t<hjGKb)?KIwR*rop^<AIIB3Q}mh!}hqDteW)rfbv&yI2vd9J}HYy^R&cN?8{so_C7~QLG"
    "-9guZ(mvo1K+o|x@Xv!Yl%<hDiIEjh9%c3j~uGsw0pW|6EOXR(rZLv0q#>N<Xg{g6;ZvbxSTVGK3f%Ppc=T?f!n%x$}E5y@&@a~p"
    "RZtcYT5&DSWWwgYHU#SZx@d0gx^R1|B+6eQa%5mm5$obyB3K4V1`YwOsNZ1?0A5v;A_a$Jh2O{nPA)@)hcg;vq4uS@yryAi31Ty1"
    "?6N^IL}ts+-"
    "jmoho+R$f))>T$h*o^}@?a&=qR5&KnQRk>CTQjfcbv5H=OeHhc|hP$iPRee~;nXx{p+b6e*VtpNJ$5gs~Y^o^M*T*I|uiGcL>C!%"
    "|-F7UecBO@`?Za_$O1t$;)5U#Qr`_6itG}j;`*28F8}-"
    "FDzfBkSYbD?%?P`&hHFllPQ(j2KCRmHHwH_+HrR{^(RJe83zLXeSk((A|X$3T)rd`ssBwMSeAxqhfqg|C-"
    "SHfd?yXz5Mm0Q>1&Gu{YuF4(D7tg6|@2;zK$KoM`{j<?kyLFl09!-^9wObd&J&Y%58>`Z->+FS|we1+yRl9Ya*++r8i-"
    "lr(o!64JyvwnQ=f@g#%t5;nF{paS_2YsuceQ6w{k(5h8N1nK3?f>thqXlU-7`I&U=2Q&;Xc-"
    "<yJ(d#$K%R7_FaJ=RK&cN;_Xq<98|^4s%vPztMP-%n2+o4u{`lzv<kVd(rS-kpFS0GU4X`zv+a3@3RyNn_T9h{36HGHl(7KYC7S@"
    "rasAVM&nEzpl)iRsw|%hcxX!;l=G|&IDkX{Qf~m#U_W4j5+h*Muc7tP7R1({9zHB}16QVNq&4B(0F99w&PFJy%-"
    "DN8;iJM7&)Remm0c5hynq#%Qn+YQ@lXx6ZYuuF+QK?B<C(iM#S>7WwS01xQ?*f%{9Xs_dP&wDJrrHH6<vRAxU7#Yawd~mks$j=QX"
    "$J!pZXIirU7+ezFg*%N(y@Zs1*$w1^Qe#{trgrpP?f2MfvQYJWt5JjipnS&Nfnh*Fp?@Nqf{hSOt>PE)G*-+L{h_qD-KBw6Rt2MH"
    "B7jYkkl~Y%0W`YgewI}4HK>mBsEUBD%0>$Q2dcP<}m{f#yl$dNFDR2*dukk8HFCH^UVMR#@?g6!vf!o0^q<mqxd&qr%=ve0Xv0K4"
    "hz^R6meL<JSyO@fO%BBVF4dkg&P(z;fgjaV!{<{Sj0Rk)v(CvQDq{hN0o_~9_1MpF+EB%EaAhYEW;9}M@fby?2i>*onRi7Vpzids"
    "0hOnCS3W&^1g}!Rhh&IS7j0=T(N~2_D5wFW~ht;3o}$kX@waoqo~3Rl~GP%hRQT}p@qsQpfE#alunqTGKwb5P#MJ%=BSJ^33F6Nf"
    "rL3KqcFl8l~E93j>;&7Fh^w+L71a5iXY4|;T>Kxa>C&yBPBd3a<CjRP?gCE167%97^uo*$3RskXAD$ja=}1VCRYqpWpcwnRR(LWq"
    "#(fxDih)5FD6{^ffY=+q65P!E-"
    "5uItm2Xq1H&pVDJ?Lp;*ydA!{RI{B(TbPRAsO@ONs^zi?gIyz_2(=N(2l`siZW(u#`%$eWGH2gv}FJb0uH^@yL_B?6+jV?g^~W67"
    "8M9ti#TU##vW+utH0)YXU2@1bZg1LQ4t)3@fw*`z5eKO9}!EE3~8_z_3C~3IeQidQ_Rt=}~1m-"
    "?b`(6<SgdU>!Rp?2W)uE;;OF!SpByaIE=~f&j;wFDVFctof3H0LPjyDF|>Z<&uH`$Ko(42ym?Vl7axonlC8`aIE=~f&h=GjDi5i;"
    "xH))@QBJN2yiS8lY#)pax*CiaI7Mef&h=4a8(AY$fO{^6DC|ifMXSz6a+Zdd`UroW6hTe?ES*@C<t(@`I3SFPn;gu^u_5>Ww7Q;3"
    "IZH!zN8?)vF1w(0vt=Zq#(etluHT%94oY>Ai%NaO9}!UE3{N$M;_);L4Z5wQI)~MD=7$YEaj4d0LKa~DF|?^(2{}xcg&-"
    "L0LM};DF|>Z<x+#)lBkS=0Otx#L4b43ry#(&LQ@dnT=OXia4zK(1UQ#+3Id!<IRydErJRBQ=Tc5VfaB}4q#(e#LQ@dnT%jolaIVl"
    "g>|Uijnt}kw3e6M*I96z;Ai%NkG6eyS^^_?HaD3Ti3IZHocA0_zubduL1`97!5a5;5qsm|@WeNfuODT)6qc~xpDubnzDF|>ZrA$G"
    "9V<}|{0vszOQxM=-bD4qw$5P4^1b9Pb6a;ujWfTNB7H6g)!148&DF|?^;!Ht+V-"
    ";r#0=%O#3IZI<JyQnY_~y=(0XWu$rVJnlPI%WqOt^tEsI@YHjCG+Y1ISnxnlgZlb)gyTzsEc(1ISoFnlgZl#hEDs$dPYGm5F>as!"
    "YUdR0fc-"
    "I5TAc8EY<suOqOOGWa$EU&tAJ8G$vI!DkWpLeAi$2rSNwK8fHwsxmyWD+9<pu`2_}NK{Q3K<4>c89?S0fHHv0^R+U7%=5J}fXq`|"
    "hR;>FMOB99LS+D%CnRM6nI|M=0GTHwWdNCHS7iX1XD(#`nI|M=0GS7SWdNCnW@P|{X9Z;dg=Yn20ELHUWdMaoTx9@-"
    "$8co;1p%8W11LO(D+4GzkSYTxJdi2_C<w1i89?C?R~bOzfm9hl!3_(h44@#BGGzb-QIj?Jt_#!C;G-@a!<7LP<7-"
    "r95Db|zfPydDO&LHzjAP0G3bGVa22haBScA{*FptUr3L+9y22hZEm@<HZK*N*)6htJZ44@$SFl7J*$%iQeC`dj`89+huVafnX=7g"
    "&<2sB(7KtZ74$^Z(!n|5UY1%ZYK_zJROpej@NX5b6RfPtz^<-"
    "1m8D&Ms#gNry<22c=axH5o(>mFAIP;e#X$^Z(!a&~0^1%ZYu11N|eTp2)VeAlWBF5*1GXQ>SXRhh;&qsrg{$&~>VTp+nJfPxIbl>"
    "rp2*j*Vw!9v`X0Tf)DxiWx?FBV-HKn;A?RRj4N^=n~V_qZ~Eith_u89>E#k1GSHxbAUf02P-"
    "rt_+}JrRfG=bo0%qGWgQYl>yYmcdg18|FkND@3~wVK*ha{t_+~!TPartQ1LyND+8$bR?3wDR9yGCGJuNjkX#u+#TPlQ44~q~?#cj"
    "a=ATw&GN(tC;fY-tKt-zH$^a_Qt{J|o=bu((cy<LB1Vr(!44^jtX;lX4wJQUtjnkvb@H_*?2Rzt=?E#PB$^aS?O;-"
    "lcc(4b*10L*^0W==$!Rvqrdu0GE@Lj9T0d6;OFgb{PGiq^w=+l(}G@fU`-"
    "hc;tFgM`AUKv2+!Co0a<IxOk4RD);D+6de>?s3iSjBk-"
    "`w32uD#PQWGJu9voGSxpJTxl<X!s`Al>sy^Q<MQT9!Qk|G#*Hm0W=;+l>sy^0h9qWUfC-HXguO7187_VC<ExMwK9N?)vzlA=v)me"
    "1L!<yDg)?T4J!laTo)<>=q#Z!fQ~5Ml>v0rIx7R{SU_fF039XF$^be}npqh@Z+wla4D#@-44`9imX!f?gwh!-"
    "214N9ZV(wUvO^?ZCin^joU=1{3Iv=(G8hU3+(MVZOd#OokikhHAT`WjBM>sTSs;?{2sEmkCD5qxy@N(LwB<zRIoOR8XvF<kkwA>x"
    ">y!z^h(%aVV49P;O|r~M7zutkIKt%w=B1Udvq2<2n@R>2&pnD%G!PTMuFlE^7T-"
    "aP1dAL56WPEY2VY`j#RGRny%eb$CFe*mm@WM4;Am7ipWtW21FeBZxXmOxXoPqxI~W=9sHm7A^4HQ?IYHzPHM4_(5x&LA4)#UH*9q"
    "oDtfsPp$lv8<g$0rKNn{7pBAyL1cmVS_ue>1g8|MrT0!KLHv4y;gRvUriG*?F%zjGM`FM*YLrD%&A**5w?ukU~O=9{m+`<IiWwe`"
    "*I`R&J>FJJ!gAHVwH`#-"
    "$=`uJB{bL*?yo!RyE#mAe`Y*_yK`r!xefBV(#Pj7EtU4LADU@UL@=;nVpfB$~9!;W^gSd;BNx9wd_pPk>{Ui|#wc4NM6%N3@L`S!"
    "il_ha|%xV$W$*>A_Q#bo%2-%G#l?}f7#N{)MbQLL-"
    "t=SxG6wi)3jXAMlq#!LczQUz&X=TTb&D^9FM0}IyB6#{VrZW@@e#SSg9(?ZZl9<XDCHu*z+6~`ye5ui@WY_|fDY%&4*@KhN=pvYc"
    "0pipFk6p$!p{vaJ9`FjV@h?krRG>XRGg+gTHuOq2V{{D}y6Wh!biT4f~1^$SuQY3##0g?Qj5@-"
    "~7rx0nxn`R=l$(t@E(mHR&rAXeE?hwgaxihuNTfQJN@XjKLoa{@{NM=peA(G#T2a4oZ*bvDeFi|AGXQN-"
    "|_h%5vlom8<*z3Gdo5(;xqm~$gYGlQ^!%3saq=wq$k{u!o7mgaq@8&aT#IFUjQzS2qA(BfC(5T?|Y8f=*9T6Ec;@v?RG~ykH1vJX"
    "olM85+@#S(MjSxZ?qc-u^L8FY@4hv|+-"
    "&>SIk$6XyejW1(8u52H1vKK%k7}ScDW5gc9bsgmU&lz$h!^}7G~(}ZD`|wU04iyOZwo7E#2@ch(1`64Drm$`7A;UDso6jy_9SVb5"
    "qsY>qhF^iHK#}#lN)Hn22Tw%Vsohm8nHoGBaLtaPa}<RHteJkj*6W$!a1&kM(p(1jUwsk=%f+u3+SK`yFzx*DB|edD@D?C)EoUeY"
    "1BcZ$ewf|P$+tKg-BP5m0U>FDi_g4p=iDqK&Xh_WO34lP;M2Z3hcKTDurTw92$kP1fW)6Q&K<<qgBi+FbCt;G7+GI1zd<npbi!?U"
    "#n9n<`uYu1$O_9q!!yFM^Y<uD5;hC0!S_Pq)en1_t!*fu?J})wb%ePky?>Wr%5gL<V>U%o4*2rNc{FV0)rT#GlOgm<p%~RMB<t~0"
    ")`l&VPcaFp*Atf*3gN&v{7i7m}P4yqcUI-BQ#D7vo(}W6phqkQfQ=>*NJVmhVr!Gq!xE=C$-"
    "od)=8}tCidAH8fFIC5E>>H+HhMl6K!a<Ol-"
    "6zwDp;hHiV{$m9~cB8ax7;7^}82vD1doIx*CS3kVZSZD_SmOtm32Pi(az)F;N;5NZ=^Z4G5(|4eG}sREhQDq&)<4WToOZ4Kr1Kq0"
    "kqp4e<_D7)eoQj3STLTa&ba3QtW2f2`1Y#v-lt%=(=sWmm-*3dAs-"
    "G*e9iSahHS|`@q5Sl0E+Yo9K`)vuWymSC)F+%Iaf*V48V#2MVe5gPrwb)7-"
    "z(wMX@)5|z2n`c6ZVlz71F(x!`Mn{)ixHY8mfRZ32c|Sqi<b_K)XHIE%ndy&Osu)#0_wz^8*VF4?75-"
    "UFfr)XQ1(Rcq!y1Zoz&vOq?20gjNVBtt_wP;#fv9E8Hqn4jKDGy)9nN-Bk|{x30Owr4=59`j1d|pw%r<9XU5$SS|`@skk^@cH?(R"
    "K`);_cGBNOmR^!CNTSF%<)uh(M`I^*XH^NA2u?u4)weVb|6iF?%z66$$*svi*Qj3jABdNviiILRe*Zz^zVhhzoYQ>qgw}!H1ZX&h"
    "VuQ!oeVP^0Rp<!b24WWEnq!t?`6U$&bl|(FqcmE|~8M(}SzM<8b(>JslCSKnf%7&Z7GBUfS63fW!rAaJ<-"
    "wP&U8JRb#5X;~<t%+C$`-"
    "mlC8JW$5iDl%8Yc;9Gdyj}^@Qc|*EF({>y`5T36Blp@jT0Ym4dt1eSOyy^CSn=v=9q|OI8VpKGT5Fn5zCm^?GnrIWD{3#Xw@fn-"
    "w+y~9cnXgaJbeoaR-OcF!2Z1&@gidhfte%ghObVxP(LK%qJW|`@|_+LMPV##4;up^29PGCkqhEuwExd;1KH156u(Ta0s=DZ#aaei"
    "F3Gy^3G0T8Iv<5h-"
    "FMp=OC6bIiG`A#^i(!Vi}V&I*4UVjvOJDF*zNDSjOaN7GfDTbrXkH!^BTqL%D<?mSGdCa8ip+*NJ8Dc~^;825;I(#4`A#uS6_^&m"
    "&93GI)naB9_5Nwk2X2e5PF@mci%bC1M$T>|Y|5!3X~(Vi|m*Um}*l8&VRn4Biiuh-"
    "L7xhlyB*#W?XChftfijzege_>OBRyD}2X;FCLzSO#yPF=81OX8z+6%Ey};u?+sm&WL63CK@A_ktY7xfkOMli5xDVPQ1u9l(&%+%S"
    "aQ?bf;F!#E~3A)5Mb;Li5CxTtnF>pI8PTG;PE(_>)W{mcb`y8?g*NJKKn5@R{L8EF+aL@hFGTnM=8b;(lc#mXX+;kyu7zn@eID$;"
    "-s8976lVuN*>c;#jVs_`Qu0%SfIkuI12bo%ohRXqh;dYv{y4oYZ1NTVfe$>R+y*Y`jY>gTEj%Vi}1)Xd#x7!pz4ULVe<74xwq{Wi"
    "FwShhkzG`~kfY%ZTioO)Mkw$pXYOB7f9FEF(_7QwkJ1b2isdK4OGe2Ky2iv5YwNH<wWM!!TkQyq(X8Wdyd;C6*C*%p#T%*z%WHM!"
    "+J<h-CyGUx{S|9yEz%1RmaqWdt7Hh-C!xiR(Fp&V0||w$jA;Tticyc%MUPo4B7ts89UQHFRPcPHM%O2Rek-"
    "i3>Vht4(~+Av8>!(BT4X;)M>OW#Wbop?TtmuAyP(hz_B7;)xESHgQFV&^GZ!htN84Mu*Ti@kWQxG;v3V&@k~we;gV+Pe#Bp;^gaE"
    "U>PGcPF&I<v`>7}A=D>M=@6PGUg;XjheQC&7@;%2bO?<T$8-"
    "n{6VG%Ft##s>4xxSGn+~CE;+ziG+9uxV5b6{6bPb&tt&>_4^LA2e@|`oO#m=#T)M9VMKx$#V<$=^<SI9tWv5R9MwY*LI)FE`{s1B"
    "iV;;9ayY2vD`q5QpdB(>0?%_FIm`ovouTFn!8bqI|Ue|5NkHgQ;o&^qy0hftrmtZOLSu_jWB4OtVZ#oxRqQY)5;+d72$#BUu!XO8"
    "O-8YZ6W8alCOC$-"
    "ov*hnp0ySSlRapJuWp=sj2E}@Ohl8w{~VdB6Jt@eorJB0egg&jic#D^V1XHM)88Yf=t5Sk`#>>AqY#E%_X4HHLpXthl|*&);?uIv"
    "z+Ccf+t8Yj-|8d_)G>=0Tf?(7g+CjRVjtzqKO4z2cyM>~Yt#HAfV!^Ec@LgU1#T|+0v^Q2Y@6SsB^<z-"
    "GLwRl02Ni8<2E~FOwZWmIE&pIfi7JF|OQp@YayB$K)#JwFtXa4PQTY2K(4xu*jaEDNzxVS@TnE1GBXqq{>Luj9PxkG50xVb~9P5j"
    "&;G)^4dAv8}s-67N`uI?Jj&O(*ciZf?-"
    "2rUzDcL<%iyF;i={M{k6O&s1elowBp)CzIp@(!VW;`0unGpBb5EfcSI39Y=!AeK>i=|C)lzcX@T8I!{^h-"
    "I)DloQLS6U%w0&@yp;*HE6hiDgt?4-"
    "m_!JaZGvV3R8+mQkxsJm8_#I&p!A&^+;hhftq5!9!@Ac)@EZPV$*p2A`~xiDmEyWSLk7e{GkEWz=jFPk6{cnV7;uXq&jgYbY)qaz"
    "wRezVOg$ofyMIs7;*VHI&V-iDmHlPnlRoWxHl#8T?sVCYCYra3hw%-"
    "^FEO8P#S6@fym0|HLwCvWZ1Jgr<o{JX~v>n8ZV?W#SSKp<!YZuc2|~6Az(zViXUdapDvYp+2#Shfte%#Y1SAn8j--"
    "`=ArcsKF<8@emp(e(?}$6T^53E$jnNETi(_2gEY?G{#IUgTD;S#4`BQ$V@C_;v`8dgTLd<#4`9h&P*(WKP1h>GWg@nOe}+s70tvl"
    "_(Rf6ETiCim`p5#zd6msGWeL*Oe}-"
    "H<IKb|_$1p*ETizuO)P`I4$Z_e3Vs)tiDj@|cqW#?NB(AF8GPPwCYDin=|C)FVn0eOgU?#d#4`B&=1eT3@FY(xgZ<hwu?#*oI}^*"
    "`qqsA%3_dVC6U!*PAR(4fc;+US!H1=1Vi|?kF2pj}I6f20;Pc-zv5dkiB4Qc*HFGAGQTRL<Vi^SyO(vF6cu7VqgFmOv#4`9B=}at"
    "xzh=(FG76t_LoB24aVx|!_!H$!ETiClmrN{!zr4=GGWf&iOe}-"
    "Hyw1cj3NN0BWn@0@hFC`CRR*yP{zf_z%gDUUA(oN(j4NUp8TV;sVi}oFdLovQ*%6soM#i^0g;++$^*|w(kt?@KYT+bbh-FNSvx#N"
    "o!l9%VE*%Q7jEqZ%LM$U^wgV@%aN;b)GWhHJLM$WWdY}-"
    "?$ha}25X;EOG77PbjBj@ev5bs>q7cjAGnERljGQ>Hq!xY`SBPa~oa76!jGWlMoz%j4s}RdzQ-MM(BjX%fh-FO7-"
    "ic*ocDg5)!KZ2!Vj1jeP>5yZ$hSpmAs;BjGBR%IEW|Q0&fJAqM#ky55X)c-"
    "h(aub%^C`^j2!r608$I5<3cQh4?!!$GA4%u5X*3+4ux2T<8)kzWjMYDDa10^*`g53aGp4cWw2XBA(p`>6cl0^Y=TjUWq9RKQj2G9"
    "Vj0eJEU^sdNuF4SW64{HW$-Zxg;<93bWALR4@xM+G8|v76k-"
    "{UMSmfd;XHE_%kaz+kXpDeqY%q*{K}>f%Wz&g5X)f8l2TADOct>W$DOK$SOz<>6k-"
    "{U)S(c|a9$A+%W(Y2r4Y+t)0RRk!|_E>si+qA0b&`BfT9q~a6VCnScW5_Da10I&%Pm+;k+axmch0)g;)l=@f2bi&Z{?K8IC)E3$Y"
    "C6g&wgC=Y<}z4Ci$gu?)w}!i87{+tw6f8GO7<A(r8YXbQ0mb`C1UGMra$#4;RdP9c`T&OwD(2Kx~eVi_LzY$H;OSDM5!*pH|X%V6"
    "iALM+1({FIJrVILrt!Nxt6SOz->Rbm;2Yr;w_gRP4yu?(A>FXa@9$1xGhVCSGpEQ39MDzOa1g<d6=VYqy(#4-"
    "%u?o?tKhWj!qu?)lIV<nbhxG1f}GA#22kXpEUtHd%aa|TE)KIV&9hGh;VwK8Xb)Z#P2h-DbA2`jM-KAyW0%V3+ON-"
    "V>iua(qtK9Y^p!i8QXmciytl~{%uXMohgHDM)|!In^!SOy=^Rf%O7F7zs~3_kU}63bwtsY)!vaG_U;Wf(4=DzOYU#j3<I*uJU~%V"
    "1NiN-TptsVcDy!}V(=mcd3-l~@M*XH{YuhOg}^u?$OmG$E;lE6qwQgPpD_u?&lxEK-"
    "XPG9;E^_=c|%%P?GN){JW5vqda}O|dGm48!GPC6>VkUX@q|8+cV>8L4x!DuwcGH3~&xiDe{2ij`OfJBU?c8SEfdiDe{SX%fp|Td-"
    "PCE$pwvGE(CVkXi^;E3u4(NU;*jNR6+R)Z!I9u?)5_tHd(c7_Ab^NW9i2mcbTgl~_i?w~>`t2HUMwVi^gyp;uxV?95h)Ww3`@C6>"
    "WvW0hD&;>CVLwXnMo%V2A`N-"
    "QJsVxL$B8>3ZX8SKnfiDe`%A&6z9%y}iXxP%~<k&x<EVi^gcY9*GDcm+=^gZ<trv5bWLwGzu<Yq&}*BXM0oEQ4+ADzOZ<hO5Lf5~"
    "A8lEF)nF(THWRja?&_k@zg&m1X?)cYk>K-FH8H`-hibKm0{p_c8SD_a)G)*FRmne)r+(?d9#Ozg)k)y}h`^zdSxhx##;m-"
    "Ov5gW3?M{z27DD>|Z@3qm451jv+t$M-"
    "Sq(_OO2h|ML4EzWL^>@BZcFa?HXf??z5fZf?(SKi+)#+u!}>_uqW`&oBS*@|fFKOWQX~hEHy<ZqMI8{O={(C)XDrZ$|dR^7q&GIz"
    "05xSGPaCy?J&0@p9RmeP=59m-F}UU)@~1zPfy~<nydqjXz$F3%I#BzkdDG$;JEg4>xybxt)#a{x{$Luvh{8-"
    "O2UM&0?ZDe(azA{>RG~r!VfqKO2AfE~d}U#~uCr;nvRHU;X*T7cY)?^!j{U>(!q>UM%zMsH9$>UtV3leZ9Z_+n=s4&d25CaS^v4K"
    "dhG*&PD<~+0*jGu$)d{e^sYwX<R`6ls{b`(b)UFtL-"
    "QEim{S=*opY*4?tMH8B70PJ!<)Phdz}b_o!kyFGs=edQ@68D}L9bt}kvr{(Q0asO4XE=}{?gkNR+Z@u#={vB-SrT=7@$T-"
    "HW1_X)rM*}Lv_y7}O%<d&WcJj^oYH9Qr#u8GoE&X*^f?8ly#pT5eqJCDTvc=_#jFaP1Ue|&Z53&+Rhmpa7avC;1P!tz199mkbN%3"
    "F)U$F#DJ6={qWaSS8(*R}uW_lnp4pm<s~sXbHi^lK~Ly`}V&kefxwLY|(CT>D0iPsx*3G-"
    "{>v_+*m@A=A_S^0=lbrRM*W;>$5Ws<^M1dh@uK)|aogH;?m3XIn+rr+t*+_fLEIE42UBr;<KaN4-8XSug+ik6-"
    "=p{gU{dM}$$X){~SrxmtEaZ&Ecf<)KVdHU9NorqVhtre%BN)0ygjvvIL|FLC;m^wW4e`_#Nxe=2f)o<`YJ{mIC~%xWQbdouFS`%@"
    "_C>FYcU%kD#gsrLOD56V(ZK8U~Ua-9v0qu{xFg?-Sro%J$Gvu6qUD-U<^EZ8E>vu+wY{Bomu&%V~x$J-"
    "tqrY|3{9&X#hS*>|w{JWRqcVF)Qc{>@+T#rkrXJcr*`Ol@xjkVE-i}QD{M(2O^?qBamiYIbb;@_zAkDQH;IO|g-"
    "o^E_jYO3+cz(eOt%f^<cBG+Qh7XPs)+pNcxt3Ung>w_2XCKK)jBk#{x6^vT%Fz$`JpLhK+6!v4+?`NTp-"
    "+q>izy3_$ds~)l&$?|M?Z>U^UHkg(Y}@(EGQ1x<c^Vx%RPFrBKR<N-"
    "J_d$|&OaWlPwM>XZ@3~J%cI$NUef8t7%VO4IXoG;a*vd!tC_pVbz8*fLBG)E`k=J%^kp6vXQ`Jk?*{2Py??az&<~bRwCBBlRCOV2"
    "2L3Ss#Qc<w_P3kCtp{tn-%jt2&)9O?+uumq{u7Od5bBsd!WgLj;rBoM?(37Q>o=oI-#2=f*&}dzd-"
    ">+=>+#>hX*}JQr}x1RdB1Pvaa|hrRjEP_nS|oL6kV=#jDus5x=Vy@5@C-"
    "L;h&I*de&RM_$=go8thZjVE<2P2rc;CaJb2Xzw<Q@KCZ)eolX*wp6(IZy;|I-;=a{gDr}pIc-"
    "l^Fmyi3u_=J3<XXL}6TjbK)evHkVbmT|r7^Uvxbd;ylF~)*XZtT;MkLl==j(%$GH09H@?;!b86H@-"
    "lgp4)HJ|E>>S@TiGRg`V_h(#Zi`gBH0%5f<wwi&r^_bwyrqH4{Ej}9_=NIb1}>gm+{bo$3x{y2|64yUc2j&j*YZu2gy_ka2+k6qQ"
    "YCVB2$^IA(N%QASA*t$t<eU#V~w5M5kI<YOZywsN4+|*-kR_N$!a>nwokL>1p8g2ad&`)zY-"
    "O~LPL!|8?>7Or)*kcmwFDEhXk~nVUmy>8klb9^@rI6VqvAt_+5|_%oZJ$=xVZ1z@#Kjz-"
    "*gl8%&EC7&A6{InDNLvCadaym{W6`VGWuI>BbB4W_ESK(>s0Xk7ZB@vtMcqWv2|E^?qB#X{l!u5`+R)LPy~7lM0S|1EG*c6r+0tX"
    "SG||QwQuxZT(M*{3Qr5(t&XL^w$HC?P|v$gKU&&`t>_``4&8ekwmw05+nPNNOGh}eU2;ASTQ`I+FO)Z*VLy(`$F=!(hx6mGb!{BC"
    "VO4$=f3!*18fV+)y2Kqj^tQcam+qs$L-"
    "LjnxHf^J#kx^{ISq3YC~B;ZRm<5|n?TXyxY4ceep(ed=5Tj2BFVZRE{%)W1d1r@#}v!Q8k<0s<$wT|eSw=m5oX;B_$ZH}%yEBV+q"
    "RfQnRUzHvKwp@D9Wsx8-"
    "3R&l0GNv!mzg8!RFH9x?~Ew7DbuWIc3?sygklYp5$ZIxoc6BS+})5YEhI~_mo=MpPwo>vlh|2Zk9wDK3Gq5S<&gT=VyCdp#-"
    "kOSJ?%MF6*0!W&iK?kTw}h_#iO}<KvSg3{NbPMDy8*8pcP^JPzZd9z_e>_~fDmyOE0$xRK0NhvS2kcThs^6+K5qhl#7Xgt6`O<1j"
    "Wp7aiEkU38dOyh<1vt%wfn&n7ys<D2Nv+3!wT>(2_qlK`@)z>Y4W0vqg!3Y{%_B#aGTB#f<2B#fOqBn-"
    "c!6BQzV?4{E<f0w7TIDZkAHI6^x)j0mpQ{(VcI9OWo=Y1N-AC_qxf6}CJ{N0Vl@kb0A$2-"
    "C`u0J!5_gCvmlDEL>LXtOMYJ0pxP}l3c<xbn9yfoDVcTqOg1NU$?)dSZR4OY3>p6Y=c7n|yVGjdZs@Ef(Jdf;T+R1e%W-"
    "Bk}<3Ut*2r>d@c;Ox?&?4bMTst0ar?^<-"
    "=xYkt<{B*QeEn@I@RSz7;yA~YiBoo7fAV=nKU+T}_(rv5#Ev^fI9@fcY^WttfTHrB$u*F;84nF+*#r4}i{pSOBSb4*;x$cXTJEni"
    "};bQ!s%iEJXa&mL>;rwR&=8u=#*!0CodTy+JapKR7^>Gc)Za9yI!*henXnEAP&y23){=&1{ZsS7y+4tDLI9cG%Goxb|ml8iAe#q#"
    "{2f@#cA5zxkq?zZ&+al5O_U?&4_{-"
    "bd%Zr<v7|#Cf=IZi`lW)KJ{`=Dh0vW^U$<5pUy14r<zquM6`R4OCZ*Tr>A#|S~f9Ziq9@~o4R{ZPQO4L?5w3R-"
    "oEu*&V&{q7EwmLM`A6jb9YUsuP{4e{0<1Y"
)
LOG_SHA256 = """
509412b720b65fc03e559a53ab12b228e2d93b8f5e67568d07e129d275089fa3  logs/audit-small.log
1a9130d0033dea9b73ff4bdaf803ace790d9d8d6900e074d96a02a32f87c9843  logs/enumerate.log
176b0615beb71d30b29083df6f7d5c092776f544bf1bd73964d360f237a890d9  logs/search-n11k11.log
b53e55d1985d1414eccf78f859bb97daf93806ad97948f163781b683ee563652  logs/search-n13k12-attempt1.log
bd428f87fbf9ff00a1c35f927a1df1fff2be4f15a2269dbaa01d9758e523bcca  logs/search-n13k12-attempt2.log
6ffcb865b1d0effe9bd27713e390204cbfaa5c43d4f0afb01084b8319930f688  logs/search-n13k12-attempt3.log
b51386271c9482c895883af2d496b8bff4ca03327e879cc5eedf8851fe3897d8  logs/search-n13k12-prefix1158-attempt1.log
78b9dc3e802b1bb7b3aeb04b320bdfdaf1037cd3815a17088532cde83c6e2439  logs/search-n13k12-prefix1158-attempt2.log
30c2fd4b49eb54360fa5b48a518d73777ed7bd1d0227c34f4945667b4b8a44f0  logs/search-n13k12-prefix1158-attempt3.log
23632f2f67fdd713e10e23cb5d5818b97bb854a0ec2e85dd2e88abbed608aa75  logs/search-n13k12-prefix1159-attempt1.log
7c68ff4c99c7f7d0a18065a541ba2995f8edc70e111491781b4df92ee0e5887d  logs/search-n13k12-prefix1159-attempt2.log
c3acb7eec5034a8b9759989b441f526ace7abc5e1449e650b766ba18f6153d01  logs/search-n13k12-prefix1161-attempt1.log
33656b24ce05846bab65234cfa1a90f278cc7c554e203c6a5671167e5521e5a4  logs/search-n13k12-prefix1161-attempt2.log
ad4e805fecc4db3bcec647a5c826df8b47e7124a5a8010a610a19dece7288bbc  logs/search-n13k12-prefix1162-attempt1.log
596be536997a3f3f1aaee68b72abbde41993bb2e14c428bd5eb94939e05f6a7e  logs/search-n13k12-prefix1163-attempt1.log
dd15d265c6571369a2668049d3c1146758a3735c1825f361b2c4219e29db2920  logs/search-n2k2.log
658ba090d45b7f4cd290a14dac8b2041c9e8e3facfbdc4e0137f71ab6d6d21e2  logs/search-n3k2.log
fc72423832a9cdc5566cda09abec9f45ba3ed967a7806659fa9daf4a4e89ac4d  logs/search-n4k4.log
aebe7c8df90a57591f6299ce90fd659a8be38161b6b5b76b002b23446100c26a  logs/search-n5k4.log
6eeec53a07e03e5c9ccb4657aa3ecda61c9ae8969b0d8774b181d01c7dedf449  logs/search-n6k6.log
4782dd446f923b15e73f6c2fa698c3bdf1c2c9c31dc5943081db94fa095df9f7  logs/search-n7k6.log
2ad244161dc2598b19a0ddc9bc8b8ba4333d7b4cc8a5257db7dc86b01a4770fb  logs/search-n8k8.log
36c8100d11a6a812bde4e18381fee480afb2117c01d2bcf186faff494d171514  logs/search-n9k9.log
06989bb5378760a71fb19b740485074a7b870bbeb645da9d2ff3b14c2543ccfe  logs/verify.log
""".strip().splitlines()

def main():
    data = json.loads(zlib.decompress(base64.b85decode(PAYLOAD)).decode("utf8"))
    dest = Path(__file__).resolve().parent / "logs"
    dest.mkdir(parents=True, exist_ok=True)
    expected = dict((row.split("  ",1)[1].removeprefix("logs/"), row.split("  ",1)[0]) for row in LOG_SHA256)
    assert set(data) == set(expected)
    for name, content in data.items():
        raw = content.encode("utf8")
        assert hashlib.sha256(raw).hexdigest() == expected[name], name
        (dest / name).write_bytes(raw)
    print(f"Restored and SHA-256-checked {len(data)} logs in {dest}")

if __name__ == "__main__":
    main()
