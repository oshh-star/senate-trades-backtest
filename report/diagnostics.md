# Report diagnostics (not registered tests)

_Built by report/diagnostics.py from data/processed/monthly_returns.csv._

- sample: 2021-09 to 2026-08, 60 months, Bloomberg-filled headline (C1)
- halves: {'design_2021-09_to_2024-02': {'r_A': {'ann_return': 0.04612550872825816, 'ann_vol': 0.2831639609929371, 'sharpe': 0.19520489131635943}, 'r_SPY': {'ann_return': 0.06430871845183406, 'ann_vol': 0.18989861522767337, 'sharpe': 0.2729302836332052}, 'r_RM_A': {'ann_return': 0.06853256590537837, 'ann_vol': 0.2807629536053554, 'sharpe': 0.27293028371682704}, 'capm_alpha': 0.011358878230258893, 'capm_t_nw': 0.11928882011581693, 'n_months': 30}, 'test_2024-03_to_2026-08': {'r_A': {'ann_return': 0.22944882266830446, 'ann_vol': 0.17465915422857384, 'sharpe': 1.0268893456023542}, 'r_SPY': {'ann_return': 0.193217605055636, 'ann_vol': 0.12124404418451884, 'sharpe': 1.1705130034745266}, 'r_RM_A': {'ann_return': 0.26584739342783625, 'ann_vol': 0.17967362222069347, 'sharpe': 1.1705130034095144}, 'capm_alpha': 0.016868886132803136, 'capm_t_nw': 0.28733398694553247, 'n_months': 30}}
- sharpe_A: 0.5025833147760869
- sharpe_SPY: 0.6130035329968303
- sharpe_diff_annual: -0.11042021822074355
- sharpe_diff_z_memmel: -0.39911821280620036
- sharpe_diff_p_memmel: 0.6898061030349687
- sharpe_diff_boot_ci95: [-0.7046573061353212, 0.36623175415358966]
- capm_alpha_annual: 0.010654604805762623
- capm_alpha_boot_ci95: [-0.09739737933816228, 0.11995216620295038]
- corr_A_SPY_excess: 0.8132484398533567
- condition_rhs_rho_x_S_SPY: 0.4985241668342679
- sharpe_gain_10pct_A_in_SPY: -0.001590628541370931
- sharpe_gain_10pct_boot_ci95: [-0.0779840629166429, 0.061746241929299554]
- share_boot_gain_positive: 0.4925
- capm_resid_vol_annual: 0.13146563813363363
- years_needed_for_t2: {'2%': 172.83214009883505, '3%': 76.81428448837114, '5%': 27.6531424158136, '10%': 6.9132856039534}
- bootstrap: {'draws': 10000, 'mean_block_months': 6, 'seed': 20261013}
