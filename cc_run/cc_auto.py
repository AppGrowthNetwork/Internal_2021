import google_cc
import cc_bq
import fb_cc

from os.path import join


def main():

    figs_fb = fb_cc.main()

    figs_adwords = google_cc.main()

    fig_list = cc_bq.main()

    
    
    with open('CC.html', 'w') as f:
        for figa in figs_adwords:
            f.write(figa.to_html(full_html=False, include_plotlyjs='cdn'))
        for figa in figs_fb:
            f.write(figa.to_html(full_html=False, include_plotlyjs='cdn'))
        for figa in fig_list:
            f.write(figa.to_html(full_html=False, include_plotlyjs='cdn'))

if __name__ == "__main__":
    main()






