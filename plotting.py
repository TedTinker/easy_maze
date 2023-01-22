# TO DO: Make it alternate between plotting normally and plotting with universal min/max.

import os 
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE" # Without this, pyplot crashes the kernal

import matplotlib.pyplot as plt 
import numpy as np

line_transparency = .5 ; fill_transparency = .1



def get_quantiles(plot_dict, name):
    xs = [i for i, x in enumerate(plot_dict[name][0]) if x != None]
    lists = np.array(plot_dict[name], dtype=float)    
    lists = lists[:,xs]
    quantile_dict = {"xs" : xs}
    quantile_dict["q20"] = np.quantile(lists, .2, 0)
    quantile_dict["med"] = np.quantile(lists, .50, 0)
    quantile_dict["q80"] = np.quantile(lists, .8, 0)
    quantile_dict["min"] = np.min(lists, 0)
    quantile_dict["max"] = np.max(lists, 0)
    return(quantile_dict)



def awesome_plot(here, quantile_dict, color, label, min_max = None):
    here.fill_between(quantile_dict["xs"], quantile_dict["min"], quantile_dict["max"], color = color, alpha = fill_transparency/2, linewidth = 0)
    here.fill_between(quantile_dict["xs"], quantile_dict["q20"], quantile_dict["q80"], color = color, alpha = fill_transparency, linewidth = 0)
    here.plot(quantile_dict["xs"], quantile_dict["med"], color = color, label = label)
    if(min_max != None): here.set_ylim([min_max[0], min_max[1]])
    
    
    
def many_min_max(min_max_list):
    mins = [min_max[0] for min_max in min_max_list]
    maxs = [min_max[1] for min_max in min_max_list]
    return((min(mins), max(maxs)))



def plots(plot_dicts, min_max_dict):
    fig, axs = plt.subplots(11, len(plot_dicts), figsize = (7*len(plot_dicts), 75))
                
    for i, plot_dict in enumerate(plot_dicts):
    
        # Cumulative rewards
        rew_dict = get_quantiles(plot_dict, "rewards")
        
        ax = axs[0,i] if len(plot_dicts) > 1 else axs[0]
        awesome_plot(ax, rew_dict, "turquoise", "Reward")
        ax.axhline(y = 0, color = 'black', linestyle = '--', alpha = .2)
        ax.set_title(plot_dict["title"] + "\nCumulative Rewards")
        
        ax = axs[1,i] if len(plot_dicts) > 1 else axs[1]
        awesome_plot(ax, rew_dict, "turquoise", "Reward", min_max_dict["rewards"])
        ax.axhline(y = 0, color = 'black', linestyle = '--', alpha = .2)
        ax.set_title(plot_dict["title"] + "\nCumulative Rewards, shared min/max")
    
    
    
        # Ending spot
        ax = axs[2,i] if len(plot_dicts) > 1 else axs[2]
        kinds = ["NONE", "BAD", "GOOD"]
        ax.scatter([0 for _ in kinds], kinds, color = (0,0,0,0))
        for spot_names in plot_dict["spot_names"]:
            ax.scatter(range(len(spot_names)), spot_names, color = "gray", alpha = .1/len(plot_dict["spot_names"]))
        ax.set_title(plot_dict["title"] + "\nEndings")
        
        
        
        # Losses
        mse_dict = get_quantiles(plot_dict, "mse")
        dkl_dict = get_quantiles(plot_dict, "dkl")
        alpha_dict = get_quantiles(plot_dict, "alpha")
        actor_dict = get_quantiles(plot_dict, "actor")
        crit1_dict = get_quantiles(plot_dict, "critic_1")
        crit2_dict = get_quantiles(plot_dict, "critic_2")
        
        ax = axs[3,i] if len(plot_dicts) > 1 else axs[3]
        awesome_plot(ax, mse_dict, "green", "MSE")
        awesome_plot(ax, dkl_dict, "red", "DKL")
        ax.legend()
        ax.set_title(plot_dict["title"] + "\nForward Losses")
        
        ax = axs[4,i] if len(plot_dicts) > 1 else axs[4]
        min_max = many_min_max([min_max_dict["mse"], min_max_dict["dkl"]])
        awesome_plot(ax, mse_dict, "green", "MSE", min_max)
        awesome_plot(ax, dkl_dict, "red", "DKL", min_max)
        ax.legend()
        ax.set_title(plot_dict["title"] + "\nForward Losses, shared min/max")
        
        ax = axs[5,i] if len(plot_dicts) > 1 else axs[5]
        awesome_plot(ax, alpha_dict, "black", "Alpha")
        ax2 = ax.twinx()
        awesome_plot(ax2, actor_dict, "red", "Actor")
        ax3 = ax.twinx()
        awesome_plot(ax3, crit1_dict, "blue", "Critic")
        awesome_plot(ax3, crit2_dict, "blue", "Critic")
        ax.legend()
        ax.set_title(plot_dict["title"] + "\nOther Losses")
        
        ax = axs[6,i] if len(plot_dicts) > 1 else axs[6]
        min_max = many_min_max([min_max_dict["critic_1"], min_max_dict["critic_2"]])
        awesome_plot(ax, alpha_dict, "black", "Alpha", min_max_dict["alpha"])
        ax2 = ax.twinx()
        awesome_plot(ax2, actor_dict, "red", "Actor", min_max_dict["actor"])
        ax3 = ax.twinx()
        awesome_plot(ax3, crit1_dict, "blue", "Critic", min_max)
        awesome_plot(ax3, crit2_dict, "blue", "Critic", min_max)
        ax.legend()
        ax.set_title(plot_dict["title"] + "\nOther Losses, shared min/max")
        
        
        
        # Extrinsic and Intrinsic rewards
        ax = axs[7,i] if len(plot_dicts) > 1 else axs[7]
        ext_dict = get_quantiles(plot_dict, "extrinsic")
        cur_dict = get_quantiles(plot_dict, "intrinsic_curiosity")
        ent_dict = get_quantiles(plot_dict, "intrinsic_entropy")
        awesome_plot(ax, ext_dict, "red", "Extrinsic")
        awesome_plot(ax, cur_dict, "green", "Curiosity")
        awesome_plot(ax, ent_dict, "blue", "Entropy")
        ax.legend()
        ax.axhline(y = 0, color = 'black', linestyle = '--', alpha = .2)
        ax.set_title(plot_dict["title"] + "\nExtrinsic and Intrinsic Rewards")
        
        ax = axs[8,i] if len(plot_dicts) > 1 else axs[8]
        min_max = many_min_max([min_max_dict["extrinsic"], min_max_dict["intrinsic_curiosity"], min_max_dict["intrinsic_entropy"]])
        ext_dict = get_quantiles(plot_dict, "extrinsic")
        cur_dict = get_quantiles(plot_dict, "intrinsic_curiosity")
        ent_dict = get_quantiles(plot_dict, "intrinsic_entropy")
        awesome_plot(ax, ext_dict, "red", "Extrinsic", min_max)
        awesome_plot(ax, cur_dict, "green", "Curiosity", min_max)
        awesome_plot(ax, ent_dict, "blue", "Entropy", min_max)
        ax.legend()
        ax.axhline(y = 0, color = 'black', linestyle = '--', alpha = .2)
        ax.set_title(plot_dict["title"] + "\nExtrinsic and Intrinsic Rewards, shared min/max")
        
        
        
        # DKL
        dkl_dict = get_quantiles(plot_dict, "dkl_change")
    
        ax = axs[9,i] if len(plot_dicts) > 1 else axs[9]
        awesome_plot(ax, dkl_dict, "green", "DKL")
        ax.set_title(plot_dict["title"] + "\nDKL")
        
        ax = axs[10,i] if len(plot_dicts) > 1 else axs[10]
        awesome_plot(ax, dkl_dict, "green", "DKL", min_max_dict["dkl_change"])
        ax.set_title(plot_dict["title"] + "\nDKL, shared min/max")

    
    
    # Done!
    plt.savefig("plot.png",bbox_inches='tight')
    plt.show()
    plt.close()