export I_WANT_EXCEL=${GITLAB_USER_NAME}
if [ -z "$I_WANT_EXCEL" ];then
    export I_WANT_EXCEL='sky_gitlab_robot'
fi

gen_xls_zte_ha28()
{
    python XlsBot/bin/Action.py --repo ha2.8 --file XlsBot/log/ha2.8_zte.xlsx --labels '客户：中兴,Done'
}

gen_xls_abc_ha28()
{
    python XlsBot/bin/Action.py --repo ha2.8 --file XlsBot/log/ha2.8_abc.xlsx --labels '客户：农行,Done'
}

case $1 in
    gen_xls)
        gen_xls_zte_ha28
        gen_xls_abc_ha28
        ;;
    *)
        exit 1
        ;;
esac