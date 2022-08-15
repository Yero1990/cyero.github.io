val = 0.


def get_simc_ref(string=''):

    simc_parm_file_path = '../cafe_online_replay/UTILS_CAFE/inp/set_basic_simc_param.inp'
    simc_parm_file = open(simc_parm_file_path)

    val = 0
    
    for line in simc_parm_file:
        if (line[0]=="#"): continue;

        if string in line:
            val = float((line.split("=")[1]).strip())
    return val
