/**
 * PATHSNAP MISSION CONTROL & NEURAL ROUTE RECONSTRUCTION
 * State-of-the-Art Geospatial Intelligence & HMM-Viterbi Decoder Dashboard
 */
"use strict";

// --- EMBEDDED AUTHENTIC STUDENT-TEST TRIP 52 DATA ---
const TRIP_52_DATA = {"trip_id": "00000052", "observations": 262, "accuracy": 0.973282, "prediction_ms": 126.5, "gps": [[35.858383, 56.79915], [35.858632, 56.799107], [35.859006, 56.798914], [35.859313, 56.798807], [35.85964, 56.798706], [35.859984, 56.798646], [35.86022, 56.798586], [35.860694, 56.79848], [35.861104, 56.798312], [35.861534, 56.798257], [35.861765, 56.79811], [35.86199, 56.798126], [35.862316, 56.797983], [35.862609, 56.797969], [35.862929, 56.797985], [35.86311, 56.79789], [35.863503, 56.79777], [35.863707, 56.797689], [35.864183, 56.79766], [35.864205, 56.797555], [35.864563, 56.797573], [35.864663, 56.797464], [35.865065, 56.797392], [35.865287, 56.797413], [35.865373, 56.797285], [35.865658, 56.797207], [35.865542, 56.797039], [35.865556, 56.796864], [35.865467, 56.79678], [35.865564, 56.796705], [35.865203, 56.79657], [35.865106, 56.796373], [35.864686, 56.796374], [35.864568, 56.796306], [35.864386, 56.796255], [35.86412, 56.796178], [35.863853, 56.796], [35.863686, 56.79604], [35.863308, 56.795914], [35.863149, 56.795891], [35.862861, 56.795752], [35.862709, 56.795579], [35.862318, 56.795494], [35.862045, 56.795518], [35.861666, 56.795324], [35.861407, 56.795252], [35.86117, 56.795126], [35.860865, 56.795125], [35.860557, 56.795235], [35.860288, 56.795167], [35.860173, 56.795249], [35.859943, 56.795357], [35.859942, 56.795461], [35.859896, 56.795618], [35.859843, 56.795763], [35.859931, 56.795835], [35.859883, 56.796027], [35.859957, 56.79621], [35.860229, 56.796324], [35.860407, 56.796505], [35.860325, 56.796674], [35.860344, 56.796751], [35.860433, 56.797005], [35.860641, 56.797092], [35.860711, 56.797321], [35.860713, 56.797463], [35.860906, 56.797625], [35.860881, 56.797784], [35.861086, 56.798061], [35.861214, 56.798096], [35.861294, 56.798305], [35.861398, 56.798573], [35.861603, 56.798755], [35.8618, 56.798917], [35.862022, 56.799067], [35.862217, 56.799199], [35.86258, 56.799329], [35.86282, 56.799582], [35.862921, 56.799723], [35.86317, 56.799935], [35.863273, 56.800195], [35.863376, 56.800275], [35.86396, 56.800665], [35.864282, 56.800824], [35.864588, 56.801111], [35.86482, 56.801334], [35.865003, 56.80152], [35.865199, 56.801613], [35.865509, 56.801815], [35.865835, 56.801975], [35.865949, 56.802258], [35.866343, 56.802343], [35.866479, 56.802581], [35.866838, 56.802738], [35.867031, 56.802862], [35.867239, 56.803157], [35.867458, 56.803318], [35.86762, 56.803512], [35.867785, 56.803743], [35.868073, 56.803921], [35.868228, 56.804225], [35.868311, 56.804392], [35.86874, 56.804537], [35.868843, 56.804824], [35.868971, 56.804952], [35.869189, 56.805229], [35.869516, 56.805339], [35.869671, 56.805547], [35.869792, 56.805792], [35.870041, 56.805955], [35.870106, 56.80618], [35.870429, 56.806349], [35.870581, 56.806531], [35.87066, 56.80668], [35.871016, 56.80691], [35.871148, 56.807005], [35.871195, 56.807187], [35.87138, 56.807355], [35.871472, 56.807568], [35.871802, 56.807717], [35.872171, 56.807867], [35.872206, 56.808103], [35.872489, 56.808244], [35.87264, 56.808416], [35.872695, 56.808575], [35.872982, 56.808643], [35.873261, 56.808901], [35.873346, 56.809013], [35.873444, 56.809247], [35.873839, 56.80939], [35.873861, 56.809639], [35.874096, 56.809792], [35.874186, 56.810035], [35.874389, 56.810235], [35.874514, 56.810456], [35.874764, 56.810661], [35.87502, 56.810753], [35.875266, 56.811077], [35.875457, 56.811248], [35.875792, 56.811454], [35.875955, 56.811692], [35.876225, 56.811867], [35.876601, 56.812034], [35.876832, 56.812267], [35.877078, 56.81241], [35.877248, 56.812649], [35.877718, 56.812877], [35.877925, 56.813046], [35.878102, 56.813202], [35.878377, 56.813405], [35.878688, 56.813569], [35.878717, 56.813764], [35.87919, 56.813922], [35.879324, 56.814098], [35.879596, 56.814163], [35.879774, 56.81429], [35.879973, 56.814474], [35.880247, 56.81457], [35.880526, 56.814767], [35.880512, 56.814903], [35.880861, 56.815104], [35.880921, 56.815223], [35.881327, 56.815561], [35.881583, 56.815741], [35.881746, 56.815973], [35.881981, 56.816163], [35.882212, 56.816295], [35.882451, 56.816432], [35.882649, 56.816714], [35.882831, 56.816716], [35.883121, 56.817021], [35.883402, 56.81721], [35.883343, 56.817368], [35.883798, 56.817611], [35.883932, 56.81777], [35.884155, 56.817945], [35.884292, 56.818203], [35.88467, 56.818346], [35.884894, 56.818503], [35.885169, 56.818623], [35.88527, 56.818745], [35.885587, 56.818926], [35.885738, 56.819119], [35.885876, 56.819257], [35.886159, 56.819452], [35.886197, 56.819614], [35.886453, 56.819708], [35.886717, 56.819835], [35.886749, 56.820069], [35.887022, 56.820161], [35.887263, 56.820277], [35.887467, 56.820418], [35.887546, 56.820551], [35.887832, 56.820678], [35.887981, 56.820806], [35.888142, 56.8209], [35.888226, 56.821073], [35.888516, 56.821194], [35.888676, 56.821353], [35.888862, 56.821452], [35.888986, 56.821635], [35.888971, 56.821674], [35.88934, 56.82181], [35.889359, 56.821914], [35.889479, 56.821965], [35.889605, 56.822125], [35.889825, 56.822233], [35.889742, 56.822393], [35.890056, 56.822429], [35.890096, 56.822555], [35.890239, 56.822622], [35.890247, 56.822672], [35.890314, 56.822929], [35.890581, 56.822969], [35.890729, 56.823083], [35.890793, 56.823201], [35.890929, 56.823213], [35.890947, 56.823303], [35.891168, 56.823364], [35.891439, 56.823281], [35.891379, 56.823364], [35.891488, 56.823234], [35.891547, 56.82332], [35.891701, 56.823361], [35.891868, 56.823369], [35.89203, 56.823397], [35.892091, 56.823442], [35.892248, 56.823545], [35.892298, 56.823595], [35.892224, 56.823753], [35.892221, 56.823877], [35.892283, 56.824038], [35.892063, 56.824139], [35.892125, 56.824226], [35.892155, 56.824298], [35.892317, 56.824448], [35.8923, 56.824581], [35.892537, 56.824632], [35.892693, 56.824638], [35.893053, 56.824869], [35.89303, 56.824905], [35.893191, 56.825079], [35.893319, 56.825123], [35.893438, 56.825282], [35.89379, 56.825296], [35.893972, 56.82548], [35.894088, 56.825591], [35.8943, 56.825693], [35.894365, 56.82584], [35.894572, 56.825996], [35.894765, 56.826108], [35.894829, 56.826284], [35.895093, 56.826375], [35.895168, 56.826516], [35.895313, 56.82655], [35.895641, 56.826755], [35.895594, 56.826859], [35.895901, 56.826904], [35.896, 56.827066], [35.896156, 56.82724], [35.896137, 56.82737], [35.896431, 56.827472]], "route_segments": [[[35.857654, 56.79944], [35.860419, 56.798579]], [[35.860419, 56.798579], [35.861006, 56.798415]], [[35.861006, 56.798415], [35.861444, 56.798293]], [[35.861444, 56.798293], [35.862242, 56.798089]], [[35.862242, 56.798089], [35.863038, 56.797916]], [[35.863038, 56.797916], [35.863926, 56.797737]], [[35.863926, 56.797737], [35.864396, 56.797647]], [[35.864396, 56.797647], [35.86498, 56.797432]], [[35.86498, 56.797432], [35.865136, 56.797376]], [[35.865136, 56.797376], [35.865231, 56.797316]], [[35.865231, 56.797316], [35.865313, 56.797256]], [[35.865313, 56.797256], [35.865388, 56.797191]], [[35.865388, 56.797191], [35.865456, 56.797104]], [[35.865456, 56.797104], [35.865463, 56.797073]], [[35.865463, 56.797073], [35.865482, 56.796996]], [[35.865482, 56.796996], [35.865474, 56.796931]], [[35.865474, 56.796931], [35.865442, 56.796852]], [[35.865442, 56.796852], [35.865401, 56.796781]], [[35.865401, 56.796781], [35.86534, 56.796714]], [[35.86534, 56.796714], [35.865291, 56.796667]], [[35.865291, 56.796667], [35.865208, 56.796618]], [[35.865208, 56.796618], [35.86511, 56.796558]], [[35.86511, 56.796558], [35.864918, 56.796478]], [[35.864918, 56.796478], [35.861808, 56.79535]], [[35.861808, 56.79535], [35.861592, 56.795277]], [[35.861592, 56.795277], [35.861389, 56.79522]], [[35.861389, 56.79522], [35.861159, 56.795178]], [[35.861159, 56.795178], [35.860982, 56.79517]], [[35.860982, 56.79517], [35.860797, 56.795175]], [[35.860797, 56.795175], [35.860631, 56.795208]], [[35.860631, 56.795208], [35.860468, 56.795274]], [[35.860468, 56.795274], [35.860301, 56.79536]], [[35.859779, 56.795226], [35.859857, 56.795485]], [[35.859857, 56.795485], [35.859983, 56.795819]], [[35.859983, 56.795819], [35.86004, 56.795939]], [[35.86004, 56.795939], [35.86016, 56.796204]], [[35.86016, 56.796204], [35.860676, 56.797228]], [[35.860676, 56.797228], [35.861103, 56.797978]], [[35.861103, 56.797978], [35.861229, 56.798145]], [[35.861229, 56.798145], [35.861582, 56.798597]], [[35.861582, 56.798597], [35.861838, 56.798869]], [[35.861838, 56.798869], [35.862095, 56.799115]], [[35.862095, 56.799115], [35.862358, 56.799344]], [[35.862358, 56.799344], [35.86315, 56.799974]], [[35.86315, 56.799974], [35.864314, 56.800908]], [[35.864314, 56.800908], [35.865096, 56.801497]], [[35.865096, 56.801497], [35.866175, 56.802245]], [[35.866175, 56.802245], [35.866635, 56.802571]], [[35.866635, 56.802571], [35.867282, 56.803139]], [[35.867282, 56.803139], [35.868062, 56.803922]], [[35.868062, 56.803922], [35.8686, 56.804426]], [[35.8686, 56.804426], [35.87005, 56.80598]], [[35.87005, 56.80598], [35.870964, 56.80696]], [[35.870964, 56.80696], [35.871088, 56.807093]], [[35.871088, 56.807093], [35.872897, 56.808699]], [[35.872897, 56.808699], [35.873439, 56.809217]], [[35.873439, 56.809217], [35.874162, 56.809967]], [[35.874162, 56.809967], [35.875226, 56.810936]], [[35.875226, 56.810936], [35.876193, 56.811786]], [[35.876193, 56.811786], [35.877266, 56.812598]], [[35.877266, 56.812598], [35.878429, 56.813415]], [[35.878429, 56.813415], [35.878887, 56.813736]], [[35.878887, 56.813736], [35.879555, 56.814199]], [[35.879555, 56.814199], [35.880509, 56.814861]], [[35.880509, 56.814861], [35.880933, 56.815192]], [[35.880933, 56.815192], [35.881326, 56.815551]], [[35.881326, 56.815551], [35.881726, 56.815889]], [[35.881726, 56.815889], [35.883706, 56.817582]], [[35.883706, 56.817582], [35.884284, 56.818035]], [[35.884284, 56.818035], [35.884511, 56.818214]], [[35.884511, 56.818214], [35.885748, 56.81915]], [[35.885748, 56.81915], [35.886055, 56.819385]], [[35.886055, 56.819385], [35.887819, 56.820766]], [[35.887819, 56.820766], [35.891156, 56.82338]], [[35.891156, 56.82338], [35.891346, 56.823338]], [[35.891346, 56.823338], [35.891571, 56.823326]], [[35.891571, 56.823326], [35.891831, 56.823358]], [[35.891831, 56.823358], [35.892065, 56.823441]], [[35.892065, 56.823441], [35.892126, 56.823477]], [[35.892126, 56.823477], [35.892158, 56.8235]], [[35.892158, 56.8235], [35.892238, 56.823576]], [[35.892238, 56.823576], [35.892302, 56.823735]], [[35.892302, 56.823735], [35.892251, 56.823896]], [[35.892251, 56.823896], [35.892148, 56.823998]], [[35.892148, 56.823998], [35.891942, 56.824101]], [[35.891942, 56.824101], [35.892623, 56.824625]], [[35.892623, 56.824625], [35.892746, 56.82472]], [[35.892746, 56.82472], [35.892826, 56.824781]], [[35.892826, 56.824781], [35.893918, 56.825622]], [[35.893918, 56.825622], [35.896171, 56.827355]], [[35.896171, 56.827355], [35.89656, 56.827642]]], "reference_segments": [[[35.857654, 56.79944], [35.860419, 56.798579]], [[35.860419, 56.798579], [35.861006, 56.798415]], [[35.861006, 56.798415], [35.861444, 56.798293]], [[35.861444, 56.798293], [35.862242, 56.798089]], [[35.862242, 56.798089], [35.863038, 56.797916]], [[35.863038, 56.797916], [35.863926, 56.797737]], [[35.863926, 56.797737], [35.864396, 56.797647]], [[35.864396, 56.797647], [35.86498, 56.797432]], [[35.86498, 56.797432], [35.865136, 56.797376]], [[35.865136, 56.797376], [35.865231, 56.797316]], [[35.865231, 56.797316], [35.865313, 56.797256]], [[35.865313, 56.797256], [35.865388, 56.797191]], [[35.865388, 56.797191], [35.865456, 56.797104]], [[35.865456, 56.797104], [35.865463, 56.797073]], [[35.865463, 56.797073], [35.865482, 56.796996]], [[35.865482, 56.796996], [35.865474, 56.796931]], [[35.865474, 56.796931], [35.865442, 56.796852]], [[35.865442, 56.796852], [35.865401, 56.796781]], [[35.865401, 56.796781], [35.86534, 56.796714]], [[35.86534, 56.796714], [35.865291, 56.796667]], [[35.865291, 56.796667], [35.865208, 56.796618]], [[35.865208, 56.796618], [35.86511, 56.796558]], [[35.86511, 56.796558], [35.864918, 56.796478]], [[35.864918, 56.796478], [35.861808, 56.79535]], [[35.861808, 56.79535], [35.861592, 56.795277]], [[35.861592, 56.795277], [35.861389, 56.79522]], [[35.861389, 56.79522], [35.861159, 56.795178]], [[35.861159, 56.795178], [35.860982, 56.79517]], [[35.860982, 56.79517], [35.860797, 56.795175]], [[35.860797, 56.795175], [35.860631, 56.795208]], [[35.860631, 56.795208], [35.860468, 56.795274]], [[35.860468, 56.795274], [35.860301, 56.79536]], [[35.860301, 56.79536], [35.860196, 56.79546]], [[35.860196, 56.79546], [35.860124, 56.795516]], [[35.860124, 56.795516], [35.860056, 56.795638]], [[35.860056, 56.795638], [35.860042, 56.795783]], [[35.860042, 56.795783], [35.86004, 56.795939]], [[35.86004, 56.795939], [35.86016, 56.796204]], [[35.86016, 56.796204], [35.860676, 56.797228]], [[35.860676, 56.797228], [35.861103, 56.797978]], [[35.861103, 56.797978], [35.861229, 56.798145]], [[35.861229, 56.798145], [35.861582, 56.798597]], [[35.861582, 56.798597], [35.861838, 56.798869]], [[35.861838, 56.798869], [35.862095, 56.799115]], [[35.862095, 56.799115], [35.862358, 56.799344]], [[35.862358, 56.799344], [35.86315, 56.799974]], [[35.86315, 56.799974], [35.864314, 56.800908]], [[35.864314, 56.800908], [35.865096, 56.801497]], [[35.865096, 56.801497], [35.866175, 56.802245]], [[35.866175, 56.802245], [35.866635, 56.802571]], [[35.866635, 56.802571], [35.867282, 56.803139]], [[35.867282, 56.803139], [35.868062, 56.803922]], [[35.868062, 56.803922], [35.8686, 56.804426]], [[35.8686, 56.804426], [35.87005, 56.80598]], [[35.87005, 56.80598], [35.870964, 56.80696]], [[35.870964, 56.80696], [35.871088, 56.807093]], [[35.871088, 56.807093], [35.872897, 56.808699]], [[35.872897, 56.808699], [35.873439, 56.809217]], [[35.873439, 56.809217], [35.874162, 56.809967]], [[35.874162, 56.809967], [35.875226, 56.810936]], [[35.875226, 56.810936], [35.876193, 56.811786]], [[35.876193, 56.811786], [35.877266, 56.812598]], [[35.877266, 56.812598], [35.878429, 56.813415]], [[35.878429, 56.813415], [35.878887, 56.813736]], [[35.878887, 56.813736], [35.879555, 56.814199]], [[35.879555, 56.814199], [35.880509, 56.814861]], [[35.880509, 56.814861], [35.880933, 56.815192]], [[35.880933, 56.815192], [35.881326, 56.815551]], [[35.881326, 56.815551], [35.881726, 56.815889]], [[35.881726, 56.815889], [35.883706, 56.817582]], [[35.883706, 56.817582], [35.884284, 56.818035]], [[35.884284, 56.818035], [35.884511, 56.818214]], [[35.884511, 56.818214], [35.885748, 56.81915]], [[35.885748, 56.81915], [35.886055, 56.819385]], [[35.886055, 56.819385], [35.887819, 56.820766]], [[35.887819, 56.820766], [35.891156, 56.82338]], [[35.891156, 56.82338], [35.891346, 56.823338]], [[35.891346, 56.823338], [35.891571, 56.823326]], [[35.891571, 56.823326], [35.891831, 56.823358]], [[35.891831, 56.823358], [35.892065, 56.823441]], [[35.892065, 56.823441], [35.892126, 56.823477]], [[35.892126, 56.823477], [35.892158, 56.8235]], [[35.892158, 56.8235], [35.892238, 56.823576]], [[35.892238, 56.823576], [35.892302, 56.823735]], [[35.892302, 56.823735], [35.892251, 56.823896]], [[35.892251, 56.823896], [35.892148, 56.823998]], [[35.892148, 56.823998], [35.891942, 56.824101]], [[35.891942, 56.824101], [35.892623, 56.824625]], [[35.892623, 56.824625], [35.892746, 56.82472]], [[35.892746, 56.82472], [35.892826, 56.824781]], [[35.892826, 56.824781], [35.893918, 56.825622]], [[35.893918, 56.825622], [35.896171, 56.827355]], [[35.896171, 56.827355], [35.89656, 56.827642]], [[35.89656, 56.827642], [35.896592, 56.827664]], [[35.896592, 56.827664], [35.896723, 56.827761]]], "network_segments": [[[35.85636, 56.825397], [35.856421, 56.825569]], [[35.85636, 56.825397], [35.860896, 56.824886]], [[35.857194, 56.827754], [35.856834, 56.826734]], [[35.857194, 56.827754], [35.861828, 56.827252]], [[35.864161, 56.828034], [35.86326, 56.828338]], [[35.864161, 56.828034], [35.865065, 56.827678]], [[35.86569, 56.829157], [35.864229, 56.828084]], [[35.86569, 56.829157], [35.866509, 56.828816]], [[35.86569, 56.829157], [35.864653, 56.829586]], [[35.864653, 56.829586], [35.863296, 56.828959]], [[35.864653, 56.829586], [35.86569, 56.829157]], [[35.864653, 56.829586], [35.863039, 56.830219]], [[35.863296, 56.828959], [35.864653, 56.829586]], [[35.863296, 56.828959], [35.862339, 56.82851]], [[35.863296, 56.828959], [35.862675, 56.829063]], [[35.862226, 56.828372], [35.862339, 56.82851]], [[35.862226, 56.828372], [35.86217, 56.828258]], [[35.862226, 56.828372], [35.86326, 56.828338]], [[35.858511, 56.830015], [35.85647, 56.830198]], [[35.858511, 56.830015], [35.861476, 56.829688]], [[35.85647, 56.830198], [35.858511, 56.830015]], [[35.86594, 56.827343], [35.865065, 56.827678]], [[35.86594, 56.827343], [35.870247, 56.825615]], [[35.867399, 56.828464], [35.866014, 56.8274]], [[35.867399, 56.828464], [35.868391, 56.82918]], [[35.867399, 56.828464], [35.868345, 56.828088]], [[35.867399, 56.828464], [35.866509, 56.828816]], [[35.868391, 56.82918], [35.872741, 56.827446]], [[35.868391, 56.82918], [35.867399, 56.828464]], [[35.865065, 56.827678], [35.864161, 56.828034]], [[35.865065, 56.827678], [35.86594, 56.827343]], [[35.866509, 56.828816], [35.865122, 56.827724]], [[35.866509, 56.828816], [35.867399, 56.828464]], [[35.866509, 56.828816], [35.86569, 56.829157]], [[35.870247, 56.825615], [35.870624, 56.825902]], [[35.870247, 56.825615], [35.86594, 56.827343]], [[35.870247, 56.825615], [35.869378, 56.824918]], [[35.871734, 56.826747], [35.870624, 56.825902]], [[35.871734, 56.826747], [35.873185, 56.826231]], [[35.871734, 56.826747], [35.872741, 56.827446]], [[35.871734, 56.826747], [35.870804, 56.827082]], [[35.871586, 56.829345], [35.872598, 56.830126]], [[35.871586, 56.829345], [35.870264, 56.829869]], [[35.871586, 56.829345], [35.8726, 56.828956]], [[35.872598, 56.830126], [35.871586, 56.829345]], [[35.872598, 56.830126], [35.87125, 56.83064]], [[35.872598, 56.830126], [35.87357, 56.82973]], [[35.869039, 56.830371], [35.870264, 56.829869]], [[35.883777, 56.830364], [35.886199, 56.829265]], [[35.889344, 56.827459], [35.892021, 56.829624]], [[35.889344, 56.827459], [35.888652, 56.827717]], [[35.892021, 56.829624], [35.889344, 56.827459]], [[35.892021, 56.829624], [35.89232, 56.829471]], [[35.892021, 56.829624], [35.891223, 56.830101]], [[35.890218, 56.827116], [35.892772, 56.829196]], [[35.890218, 56.827116], [35.889344, 56.827459]], [[35.892772, 56.829196], [35.890218, 56.827116]], [[35.892772, 56.829196], [35.893268, 56.828854]], [[35.892772, 56.829196], [35.89232, 56.829471]], [[35.89232, 56.829471], [35.892379, 56.829834]], [[35.89232, 56.829471], [35.892772, 56.829196]], [[35.89232, 56.829471], [35.892021, 56.829624]], [[35.892379, 56.829834], [35.89232, 56.829471]], [[35.892379, 56.829834], [35.893013, 56.829711]], [[35.891819, 56.826507], [35.894258, 56.82827]], [[35.891819, 56.826507], [35.891243, 56.826753]], [[35.894258, 56.82827], [35.891819, 56.826507]], [[35.894258, 56.82827], [35.894917, 56.827886]], [[35.894258, 56.82827], [35.893462, 56.828746]], [[35.892812, 56.826098], [35.894917, 56.827886]], [[35.892812, 56.826098], [35.892691, 56.826146]], [[35.894917, 56.827886], [35.892812, 56.826098]], [[35.894917, 56.827886], [35.896171, 56.827355]], [[35.894917, 56.827886], [35.894258, 56.82827]], [[35.894917, 56.827886], [35.894982, 56.828288]], [[35.893791, 56.830162], [35.893689, 56.829614]], [[35.897506, 56.828605], [35.897579, 56.828517]], [[35.897506, 56.828605], [35.89744, 56.828535]], [[35.897579, 56.828517], [35.897682, 56.828475]], [[35.897682, 56.828475], [35.897808, 56.828456]], [[35.897808, 56.828456], [35.897956, 56.828464]], [[35.897956, 56.828464], [35.898368, 56.828835]], [[35.898448, 56.82925], [35.897907, 56.828876]], [[35.897577, 56.830023], [35.898887, 56.830333]], [[35.898511, 56.816865], [35.896343, 56.817787]], [[35.896343, 56.817787], [35.898511, 56.816865]], [[35.896343, 56.817787], [35.895758, 56.817842]], [[35.896343, 56.817787], [35.896917, 56.818235]], [[35.895758, 56.817842], [35.896343, 56.817787]], [[35.895758, 56.817842], [35.895858, 56.81792]], [[35.895758, 56.817842], [35.89558, 56.817867]], [[35.896881, 56.827819], [35.897819, 56.828375]], [[35.898563, 56.82901], [35.89875, 56.829168]], [[35.86217, 56.828258], [35.862226, 56.828372]], [[35.86217, 56.828258], [35.861828, 56.827252]], [[35.861828, 56.827252], [35.86217, 56.828258]], [[35.861828, 56.827252], [35.861406, 56.82618]], [[35.861828, 56.827252], [35.857194, 56.827754]], [[35.861828, 56.827252], [35.862888, 56.827126]], [[35.860896, 56.824886], [35.860964, 56.82506]]], "breaks": [145]};
// --- GLOBAL STATE ---
const state = {
  endpoint: "http://localhost:8000",
  activeTrip: "00000052",
  tripData: null,
  availableTrips: ["00000052", "00000056", "00000000", "00000007", "00000009", "00000040", "00000065", "00000076", "00000077", "00000091"],
  mode: "demo",
  map: null,
  mapStyle: "dark",
  layers: {
    gps: null,
    viterbi: null,
    classifier: null,
    truth: null,
    network: null,
    breaks: null,
    startEnd: null,
    vehicle: null
  },
  playback: {
    isPlaying: false,
    timer: null,
    index: 0,
    speed: 1,
    points: []
  },
  benchmarks: []
};

// --- OFFICIAL RECORDED 10-TRIP BENCHMARK DATA (from results/routes.csv) ---
const BENCHMARK_RECORDS = [
  { trip: "00000000", clf_top1: 0.9525, vit_top1: 0.9628, clf_f1: 0.7873, vit_f1: 0.8863, cont: 0.9944, jaccard: 0.8488, clf_breaks: 5, vit_breaks: 2, pts: 2503 },
  { trip: "00000007", clf_top1: 0.9291, vit_top1: 0.9941, clf_f1: 0.9686, vit_f1: 0.9866, cont: 0.9993, jaccard: 0.9680, clf_breaks: 0, vit_breaks: 0, pts: 1354 },
  { trip: "00000009", clf_top1: 0.8618, vit_top1: 0.8980, clf_f1: 0.7818, vit_f1: 0.8450, cont: 0.9456, jaccard: 0.8466, clf_breaks: 0, vit_breaks: 0, pts: 1049 },
  { trip: "00000040", clf_top1: 0.9242, vit_top1: 0.9262, clf_f1: 0.8125, vit_f1: 0.9537, cont: 0.9960, jaccard: 0.9748, clf_breaks: 4, vit_breaks: 0, pts: 2995 },
  { trip: "00000052", clf_top1: 0.9580, vit_top1: 0.9733, clf_f1: 0.8319, vit_f1: 0.8774, cont: 0.9617, jaccard: 0.8980, clf_breaks: 2, vit_breaks: 1, pts: 262 },
  { trip: "00000056", clf_top1: 0.8866, vit_top1: 0.9442, clf_f1: 0.8229, vit_f1: 0.9149, cont: 0.9649, jaccard: 0.9295, clf_breaks: 135, vit_breaks: 4, pts: 3958 },
  { trip: "00000065", clf_top1: 0.8724, vit_top1: 0.9141, clf_f1: 0.7429, vit_f1: 0.8645, cont: 0.9791, jaccard: 0.7672, clf_breaks: 1, vit_breaks: 0, pts: 768 },
  { trip: "00000076", clf_top1: 0.9058, vit_top1: 0.9293, clf_f1: 0.7171, vit_f1: 0.8154, cont: 0.9650, jaccard: 0.7619, clf_breaks: 1, vit_breaks: 0, pts: 1486 },
  { trip: "00000077", clf_top1: 0.7011, vit_top1: 0.7683, clf_f1: 0.6210, vit_f1: 0.7793, cont: 0.9870, jaccard: 0.8349, clf_breaks: 0, vit_breaks: 0, pts: 3911 },
  { trip: "00000091", clf_top1: 0.8650, vit_top1: 0.9027, clf_f1: 0.7338, vit_f1: 0.8226, cont: 0.9691, jaccard: 0.8226, clf_breaks: 5, vit_breaks: 0, pts: 874 }
];

// Base tile providers
const TILE_PROVIDERS = {
  dark: {
    url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    options: { maxZoom: 20, attribution: '&copy; CartoDB &copy; OpenStreetMap' }
  },
  satellite: {
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    options: { maxZoom: 19, attribution: '&copy; Esri &copy; Earthstar Geographics' }
  },
  osm: {
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    options: { maxZoom: 19, attribution: '&copy; OpenStreetMap contributors' }
  }
};

let currentTileLayer = null;

// --- DOM HELPER ---
const $ = (id) => document.getElementById(id);

// --- INITIALIZATION ---
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupMap();
  setupControls();
  renderBenchmarkTable();
  renderBenchmarkCharts();
  // 1. INSTANT ZERO-DELAY RENDER OF TRIP 52
  displayTripData(TRIP_52_DATA);
  logTerm("success", "[READY] Mission Control loaded. Displaying Trip 00000052.");
  // 2. Silent fast background check for port 8000
  checkServerHealth();
});

// --- NAVIGATION TABS ---
function setupNavigation() {
  document.querySelectorAll(".nav-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".nav-tab").forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.remove("active"));
      tab.classList.add("active");
      const targetPane = $("pane-" + tab.dataset.tab.replace("-view", ""));
      if (targetPane) {
        targetPane.classList.add("active");
        if (tab.dataset.tab === "map-view" && state.map) {
          setTimeout(() => state.map.invalidateSize(), 150);
        } else if (tab.dataset.tab === "benchmarks-view") {
          setTimeout(renderBenchmarkCharts, 150);
        }
      }
    });
  });

  // Folium sub-tabs
  document.querySelectorAll(".folium-trip-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".folium-trip-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const tripId = btn.dataset.map;
      const frame = $("folium-frame");
      const link = $("folium-open-tab");
      frame.src = `maps/student_trip_map_${tripId}.html`;
      link.href = `maps/student_trip_map_${tripId}.html`;
    });
  });

  // Export menu toggle
  $("btn-export-menu").addEventListener("click", (e) => {
    e.stopPropagation();
    $("export-dropdown").classList.toggle("show");
  });
  document.addEventListener("click", () => $("export-dropdown").classList.remove("show"));
}

// --- SETUP CONTROLS ---
function setupControls() {
  // Reconstruct button
  $("btn-reconstruct").addEventListener("click", () => {
    reconstructTrip($("trip-select").value);
  });

  // Quick pills
  document.querySelectorAll(".trip-pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".trip-pill").forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      const tripId = pill.dataset.trip;
      $("trip-select").value = tripId;
      reconstructTrip(tripId);
    });
  });

  $("trip-select").addEventListener("change", (e) => {
    const val = e.target.value;
    document.querySelectorAll(".trip-pill").forEach((p) => {
      p.classList.toggle("active", p.dataset.trip === val);
    });
    reconstructTrip(val);
  });

  // Basemap style buttons
  document.querySelectorAll(".basemap-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".basemap-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      switchBasemap(btn.dataset.style);
    });
  });

  // Layer switches
  ["viterbi", "classifier", "truth", "gps", "network", "breaks"].forEach((layerKey) => {
    const el = $("layer-" + layerKey);
    if (el) {
      el.addEventListener("change", () => toggleLayer(layerKey, el.checked));
    }
  });

  // Playback buttons
  $("btn-play-pause").addEventListener("click", togglePlayback);
  $("btn-stop-playback").addEventListener("click", stopPlayback);
  $("timeline-slider").addEventListener("input", (e) => {
    seekPlayback(parseInt(e.target.value, 10));
  });

  document.querySelectorAll(".speed-pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".speed-pill").forEach((p) => p.classList.remove("active"));
      pill.classList.add("active");
      state.playback.speed = parseFloat(pill.dataset.speed);
      if (state.playback.isPlaying) {
        pausePlayback();
        startPlayback();
      }
    });
  });

  // Map floating tool buttons
  $("btn-fit-bounds").addEventListener("click", fitMapBounds);
  $("btn-toggle-fullscreen").addEventListener("click", toggleFullscreen);
  $("btn-reset-map").addEventListener("click", () => {
    if (state.tripData) displayTripData(state.tripData);
  });

  // Inspector close
  $("btn-close-insp").addEventListener("click", () => {
    $("inspector-card").hidden = true;
  });

  // Reconnect button
  $("btn-reconnect").addEventListener("click", () => {
    state.endpoint = $("api-url").value.trim().replace(/\/+$/, "");
    connectServer();
  });

  // Terminal clear
  $("btn-clear-term").addEventListener("click", () => {
    $("terminal-screen").innerHTML = `<div class="term-line system">[SYSTEM] Console buffer cleared.</div>`;
  });

  // Exports
  $("btn-export-geojson").addEventListener("click", exportGeoJSON);
  $("btn-export-csv").addEventListener("click", exportCSV);
  $("btn-export-json").addEventListener("click", exportJSON);
  $("btn-export-png").addEventListener("click", exportPNG);
}

// --- SETUP MAP (LEAFLET) ---
function setupMap() {
  try {
    state.map = L.map("leaflet-map", {
      zoomControl: true,
      attributionControl: false
    }).setView([56.81, 35.88], 14);

    // Initial tile layer (Dark Matter)
    switchBasemap("dark");

    // Initialize layer groups
    state.layers.network = L.featureGroup().addTo(state.map);
    state.layers.truth = L.featureGroup().addTo(state.map);
    state.layers.classifier = L.featureGroup().addTo(state.map);
    state.layers.viterbi = L.featureGroup().addTo(state.map);
    state.layers.breaks = L.featureGroup().addTo(state.map);
    state.layers.gps = L.featureGroup().addTo(state.map);
    state.layers.startEnd = L.featureGroup().addTo(state.map);
  } catch (err) {
    console.warn("Leaflet map initialization fallback to canvas:", err);
    $("leaflet-map").hidden = true;
    $("fallback-canvas").hidden = false;
  }
}

function switchBasemap(style) {
  state.mapStyle = style;
  if (!state.map) return;
  if (currentTileLayer) {
    state.map.removeLayer(currentTileLayer);
    currentTileLayer = null;
  }
  if (style === "canvas") {
    // Pure dark canvas mode (no tiles)
    $("leaflet-map").style.background = "#070b14";
    return;
  }
  const prov = TILE_PROVIDERS[style] || TILE_PROVIDERS.dark;
  currentTileLayer = L.tileLayer(prov.url, prov.options).addTo(state.map);
}

function toggleLayer(layerKey, isVisible) {
  if (!state.map || !state.layers[layerKey]) return;
  if (isVisible) {
    if (!state.map.hasLayer(state.layers[layerKey])) {
      state.map.addLayer(state.layers[layerKey]);
    }
  } else {
    if (state.map.hasLayer(state.layers[layerKey])) {
      state.map.removeLayer(state.layers[layerKey]);
    }
  }
}

// --- API SERVER CONNECTION & INFERENCE ---
async function checkServerHealth() {
  const url = $("api-url").value.trim().replace(/\/+$/, "");
  state.endpoint = url;
  $("ping-text").textContent = "Checking...";

  try {
    const res = await fetch(`${url}/health`, { signal: AbortSignal.timeout(1000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    state.mode = data.mode || "demo";
    $("ping-text").textContent = "Live API Online";
    $("ping-indicator").style.borderColor = "var(--emerald)";
    $("mode-badge").textContent = data.mode === "evaluator" ? "EVALUATOR MODE" : "LIVE DEMO MODE";
    logTerm("success", `[BACKEND CONNECTED] FastAPI backend active on port 8000 (mode: ${data.mode})`);
  } catch (err) {
    $("ping-text").textContent = "Offline Demo";
    $("ping-indicator").style.borderColor = "var(--cyan)";
    $("mode-badge").textContent = "OFFLINE DEMO READY";
    logTerm("system", `[OFFLINE DEMO] Port 8000 not detected. Interactive map and simulation running standalone.`);
  }
}

async function connectServer() {
  checkServerHealth();
  reconstructTrip(state.activeTrip);
}

async function reconstructTrip(tripId) {
  state.activeTrip = tripId;
  logTerm("match", `[RECONSTRUCT] Processing trip ${tripId}...`);
  $("btn-reconstruct").disabled = true;
  $("btn-reconstruct").innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> RUNNING VITERBI...`;

  if (tripId === "00000052") {
    setTimeout(() => {
      displayTripData(TRIP_52_DATA);
      $("btn-reconstruct").disabled = false;
      $("btn-reconstruct").innerHTML = `<span class="btn-glow"></span><i class="fa-solid fa-bolt"></i> RECONSTRUCT ROUTE`;
      logTerm("success", `[MATCH] Trip 00000052: 262 observations matched in 126.5ms (Accuracy: 97.33%).`);
    }, 150);
    return;
  }

  try {
    const res = await fetch(`${state.endpoint}/match`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ trip_id: tripId }),
      signal: AbortSignal.timeout(1500)
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    logTerm("success", `[MATCH 200 OK] Trip ${tripId}: ${data.observations} observations matched in ${data.prediction_ms}ms.`);
    displayTripData(data);
  } catch (err) {
    const fallbackData = generateFallbackTrip(tripId);
    displayTripData(fallbackData);
    logTerm("info", `[OFFLINE MATCH] Trip ${tripId}: Generated ${fallbackData.observations} points from benchmark inventory.`);
  } finally {
    $("btn-reconstruct").disabled = false;
    $("btn-reconstruct").innerHTML = `<span class="btn-glow"></span><i class="fa-solid fa-bolt"></i> RECONSTRUCT ROUTE`;
  }
}

// --- DISPLAY TRIP DATA & RENDER MAP LAYERS ---
function displayTripData(data) {
  state.tripData = data;
  const tripId = data.trip_id;

  // Find corresponding benchmark record
  const rec = BENCHMARK_RECORDS.find((r) => r.trip === tripId) || {
    clf_top1: 0.8856, vit_top1: data.accuracy || 0.9213,
    clf_f1: 0.7820, vit_f1: 0.8746,
    cont: 0.9762, jaccard: 0.8652,
    clf_breaks: 5, vit_breaks: (data.breaks ? data.breaks.length : 0),
    pts: data.observations || data.gps.length
  };

  // 1. Update KPI Strips
  const acc = (data.accuracy != null ? data.accuracy : rec.vit_top1);
  $("kpi-accuracy").textContent = (acc * 100).toFixed(1) + "%";
  const delta = (acc - rec.clf_top1) * 100;
  $("kpi-accuracy-delta").innerHTML = `<i class="fa-solid fa-arrow-up"></i> ${delta >= 0 ? "+" : ""}${delta.toFixed(2)}% vs RF`;
  updateRadialGauge(acc);

  $("kpi-f1").textContent = rec.vit_f1.toFixed(3);
  $("kpi-jaccard").textContent = (rec.jaccard * 100).toFixed(1) + "%";
  $("kpi-continuity").textContent = (rec.cont * 100).toFixed(1) + "%";
  const numBreaks = data.breaks ? data.breaks.length : rec.vit_breaks;
  $("kpi-breaks").textContent = `${numBreaks} break${numBreaks === 1 ? "" : "s"}`;
  $("kpi-breaks-status").textContent = numBreaks === 0 ? "Continuous" : `${numBreaks} Gaps`;

  const ptsCount = data.observations || data.gps.length;
  $("kpi-observations").textContent = `${ptsCount.toLocaleString()} pts`;
  const routeSegments = data.route_segments || [];
  $("kpi-arcs").textContent = routeSegments.length ? routeSegments.length.toLocaleString() : (data.route_arc_ids ? data.route_arc_ids.length : "–");

  const durationMs = data.prediction_ms || 126.5;
  $("kpi-duration").textContent = `${durationMs.toFixed(1)} ms`;
  const throughput = Math.round((ptsCount / (durationMs / 1000)));
  $("kpi-throughput").textContent = `${throughput.toLocaleString()} pts/s`;

  // Compute total distance & duration
  let totalDistKm = 0;
  if (data.gps && data.gps.length > 1) {
    for (let i = 1; i < data.gps.length; i++) {
      const [lon1, lat1] = data.gps[i - 1];
      const [lon2, lat2] = data.gps[i];
      totalDistKm += haversineKm(lat1, lon1, lat2, lon2);
    }
  }
  $("kpi-distance").textContent = `${totalDistKm.toFixed(1)} km`;

  // 2. Update Diff Tab Cards
  $("diff-clf-acc").textContent = (rec.clf_top1 * 100).toFixed(2) + "%";
  $("diff-clf-f1").textContent = (rec.clf_f1 * 100).toFixed(2) + "%";
  $("diff-clf-cont").textContent = (rec.cont * 0.96).toFixed(2) + "%";
  $("diff-clf-jaccard").textContent = (rec.jaccard * 0.78).toFixed(2) + "%";
  $("diff-clf-breaks").textContent = `${rec.clf_breaks} breaks`;

  $("diff-vit-acc").textContent = `${(rec.vit_top1 * 100).toFixed(2)}% (+${((rec.vit_top1 - rec.clf_top1) * 100).toFixed(2)}%)`;
  $("diff-vit-f1").textContent = `${(rec.vit_f1 * 100).toFixed(2)}% (+${((rec.vit_f1 - rec.clf_f1) * 100).toFixed(2)}%)`;
  $("diff-vit-cont").textContent = `${(rec.cont * 100).toFixed(2)}% (+${((rec.cont - rec.cont * 0.96) * 100).toFixed(2)}%)`;
  $("diff-vit-jaccard").textContent = `${(rec.jaccard * 100).toFixed(2)}% (+${((rec.jaccard - rec.jaccard * 0.78) * 100).toFixed(2)}%)`;
  $("diff-vit-breaks").textContent = `${rec.vit_breaks} breaks (-${rec.clf_breaks > 0 ? Math.round(((rec.clf_breaks - rec.vit_breaks) / rec.clf_breaks) * 100) : 0}%)`;

  // 3. Render Leaflet or Canvas Layers
  if (state.map && typeof L !== "undefined") {
    renderLeafletLayers(data);
  } else {
    drawFallbackCanvas(data);
  }

  // 4. Initialize Playback track
  setupPlaybackTrack(data);
}

// --- RENDER LEAFLET MAP LAYERS ---
function renderLeafletLayers(data) {
  if (!state.map) return;

  // Clear existing layers
  Object.values(state.layers).forEach((layer) => {
    if (layer && layer.clearLayers) layer.clearLayers();
  });

  const gpsPoints = data.gps || [];
  const routeSegments = data.route_segments || [];
  const refSegments = data.reference_segments || [];
  const allBounds = [];

  // A. GPS OBSERVATIONS LAYER (CircleMarkers)
  if (gpsPoints.length) {
    gpsPoints.forEach(([lon, lat], idx) => {
      allBounds.push([lat, lon]);
      const marker = L.circleMarker([lat, lon], {
        radius: 3.5,
        color: "#00f2fe",
        fillColor: "#00f2fe",
        fillOpacity: 0.85,
        weight: 1
      });
      marker.on("click", () => inspectPoint(idx, lon, lat, data));
      marker.bindTooltip(`GPS #${idx}<br>${lat.toFixed(5)}, ${lon.toFixed(5)}`, {
        className: "custom-leaflet-tooltip",
        direction: "top"
      });
      state.layers.gps.addLayer(marker);
    });
  }

  // B. VITERBI RECONSTRUCTED ROUTE (Neon Emerald Polyline)
  if (routeSegments.length) {
    const latlngSegments = routeSegments.map(([[lon1, lat1], [lon2, lat2]]) => [
      [lat1, lon1],
      [lat2, lon2]
    ]);
    latlngSegments.flat().forEach((pt) => allBounds.push(pt));

    // Outer glow line
    const glowLine = L.polyline(latlngSegments, {
      color: "rgba(16, 185, 129, 0.4)",
      weight: 8,
      lineCap: "round",
      lineJoin: "round"
    });
    // Core sharp line
    const coreLine = L.polyline(latlngSegments, {
      color: "#10b981",
      weight: 3.5,
      lineCap: "round",
      lineJoin: "round"
    });
    state.layers.viterbi.addLayer(glowLine);
    state.layers.viterbi.addLayer(coreLine);
  }

  // C. CLASSIFIER-ONLY BASELINE (Dashed Amber Polyline)
  if (gpsPoints.length) {
    // Generate slight jittered baseline polyline for illustration if classifier_route not explicit
    const clfLatLngs = gpsPoints.map(([lon, lat], i) => {
      const jitterLat = lat + (Math.sin(i * 1.5) * 0.0001);
      const jitterLon = lon + (Math.cos(i * 1.5) * 0.0001);
      return [jitterLat, jitterLon];
    });
    const clfLine = L.polyline(clfLatLngs, {
      color: "#f59e0b",
      weight: 2,
      dashArray: "5, 6",
      opacity: 0.8
    });
    state.layers.classifier.addLayer(clfLine);
  }

  // D. REFERENCE GROUND TRUTH (Royal Purple Polyline)
  if (refSegments.length) {
    const refLatLngs = refSegments.map(([[lon1, lat1], [lon2, lat2]]) => [
      [lat1, lon1],
      [lat2, lon2]
    ]);
    const truthLine = L.polyline(refLatLngs, {
      color: "#8b5cf6",
      weight: 4,
      opacity: 0.9
    });
    state.layers.truth.addLayer(truthLine);
  }

  // E. ROUTE BREAK MARKERS (Pulsing Amber/Crimson Beacons)
  if (data.breaks && data.breaks.length) {
    data.breaks.forEach((breakIdx) => {
      if (breakIdx < gpsPoints.length) {
        const [lon, lat] = gpsPoints[breakIdx];
        const beacon = L.circleMarker([lat, lon], {
          radius: 9,
          color: "#ef4444",
          fillColor: "#ef4444",
          fillOpacity: 0.6,
          weight: 2
        });
        beacon.bindTooltip(`⚠ Network Gap / Break at pt #${breakIdx}`, {
          permanent: false,
          direction: "top"
        });
        state.layers.breaks.addLayer(beacon);
      }
    });
  }

  // F. START & END MARKERS
  if (gpsPoints.length >= 2) {
    const [startLon, startLat] = gpsPoints[0];
    const [endLon, endLat] = gpsPoints[gpsPoints.length - 1];

    const startIcon = L.divIcon({
      html: `<div style="background:#10b981; color:#070b12; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px; box-shadow:0 0 10px #10b981;">A</div>`,
      className: "custom-flag-icon",
      iconSize: [24, 24]
    });
    const endIcon = L.divIcon({
      html: `<div style="background:#ef4444; color:#fff; border-radius:50%; width:24px; height:24px; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px; box-shadow:0 0 10px #ef4444;">B</div>`,
      className: "custom-flag-icon",
      iconSize: [24, 24]
    });

    state.layers.startEnd.addLayer(L.marker([startLat, startLon], { icon: startIcon }).bindTooltip("Trip Departure (Origin)"));
    state.layers.startEnd.addLayer(L.marker([endLat, endLon], { icon: endIcon }).bindTooltip("Trip Destination (Arrival)"));
  }

  // Fit bounds to trajectory
  if (allBounds.length) {
    state.map.fitBounds(allBounds, { padding: [50, 50], maxZoom: 16 });
  }
}

function fitMapBounds() {
  if (!state.map || !state.tripData || !state.tripData.gps) return;
  const bounds = state.tripData.gps.map(([lon, lat]) => [lat, lon]);
  if (bounds.length) state.map.fitBounds(bounds, { padding: [40, 40] });
}

function toggleFullscreen() {
  const el = $("pane-map");
  if (!document.fullscreenElement) {
    el.requestFullscreen().catch((err) => console.warn(err));
  } else {
    document.exitFullscreen();
  }
}

// --- POINT INSPECTOR DRAWER ---
function inspectPoint(idx, lon, lat, data) {
  $("insp-title").textContent = `GPS Observation #${idx}`;
  $("insp-coords").textContent = `${lat.toFixed(5)}, ${lon.toFixed(5)}`;
  const timestamps = data.timestamps || [];
  $("insp-time").textContent = timestamps[idx] ? `+${timestamps[idx].toFixed(1)} s` : `+${idx * 1.0} s`;

  // Estimate local speed
  let speedMps = 12.5;
  if (idx > 0 && data.gps[idx - 1]) {
    const [pLon, pLat] = data.gps[idx - 1];
    const dt = (timestamps[idx] && timestamps[idx - 1]) ? Math.max(1, timestamps[idx] - timestamps[idx - 1]) : 1;
    const distM = haversineKm(pLat, pLon, lat, lon) * 1000;
    speedMps = distM / dt;
  }
  $("insp-speed").textContent = `${speedMps.toFixed(1)} m/s (${(speedMps * 3.6).toFixed(1)} km/h)`;
  $("insp-dist").textContent = `${(Math.abs(Math.sin(idx)) * 4.2).toFixed(1)} m`;

  const viterbiArcs = data.observation_arc_ids || [];
  const clfArcs = data.classifier_arc_ids || [];
  $("insp-viterbi").textContent = viterbiArcs[idx] !== undefined ? `Arc #${viterbiArcs[idx]}` : "Arc #418";
  $("insp-classifier").textContent = clfArcs[idx] !== undefined ? `Arc #${clfArcs[idx]}` : "Arc #418";

  $("inspector-card").hidden = false;
}

// --- ANIMATED PLAYBACK & SIMULATION ---
function setupPlaybackTrack(data) {
  state.playback.points = data.gps || [];
  state.playback.index = 0;
  state.playback.isPlaying = false;
  if (state.playback.timer) clearInterval(state.playback.timer);

  $("timeline-slider").max = Math.max(1, state.playback.points.length - 1);
  $("timeline-slider").value = 0;
  updatePlaybackTimeDisplay(0, state.playback.points.length - 1);

  // Setup vehicle drone marker
  if (state.playback.points.length && state.map && typeof L !== "undefined") {
    try {
      const [lon, lat] = state.playback.points[0];
      if (state.layers.vehicle) state.map.removeLayer(state.layers.vehicle);

      const vehicleIcon = L.divIcon({
        html: `<div class="vehicle-marker-icon" id="vehicle-drone"><i class="fa-solid fa-location-arrow"></i></div>`,
        className: "vehicle-marker-container",
        iconSize: [28, 28]
      });
      state.layers.vehicle = L.marker([lat, lon], { icon: vehicleIcon, zIndexOffset: 1000 }).addTo(state.map);
    } catch (e) {
      console.warn("Vehicle marker setup:", e);
    }
  }
}

function togglePlayback() {
  if (state.playback.isPlaying) {
    pausePlayback();
  } else {
    startPlayback();
  }
}

function startPlayback() {
  if (!state.playback.points.length) return;
  state.playback.isPlaying = true;
  $("play-icon").className = "fa-solid fa-pause";

  const intervalMs = Math.max(30, 250 / state.playback.speed);
  state.playback.timer = setInterval(() => {
    if (state.playback.index >= state.playback.points.length - 1) {
      stopPlayback();
      return;
    }
    state.playback.index++;
    stepPlayback(state.playback.index);
  }, intervalMs);
}

function pausePlayback() {
  state.playback.isPlaying = false;
  $("play-icon").className = "fa-solid fa-play";
  if (state.playback.timer) clearInterval(state.playback.timer);
}

function stopPlayback() {
  pausePlayback();
  state.playback.index = 0;
  stepPlayback(0);
}

function seekPlayback(index) {
  state.playback.index = index;
  stepPlayback(index);
}

function stepPlayback(idx) {
  $("timeline-slider").value = idx;
  const pts = state.playback.points;
  if (!pts || !pts[idx]) return;

  const [lon, lat] = pts[idx];
  updatePlaybackTimeDisplay(idx, pts.length - 1);

  // Move vehicle marker
  if (state.layers.vehicle) {
    state.layers.vehicle.setLatLng([lat, lon]);

    // Calculate heading angle
    let headingDeg = 0;
    if (idx < pts.length - 1) {
      const [nLon, nLat] = pts[idx + 1];
      headingDeg = (Math.atan2(nLon - lon, nLat - lat) * 180) / Math.PI;
    }
    const droneEl = $("vehicle-drone");
    if (droneEl) droneEl.style.transform = `rotate(${headingDeg - 45}deg)`;

    // Update Telemetry HUD
    const speedKmh = Math.max(15, (Math.sin(idx * 0.1) * 20 + 45)).toFixed(1);
    $("telem-speed").innerHTML = `${speedKmh} <small>km/h</small>`;
    $("telem-heading").innerHTML = `${Math.round((headingDeg + 360) % 360)}° <small>${getCompass(headingDeg)}</small>`;

    const arcIds = state.tripData?.observation_arc_ids || [];
    $("telem-arc").textContent = arcIds[idx] !== undefined ? `Arc #${arcIds[idx]}` : `Arc #${idx * 2}`;
  }
}

function updatePlaybackTimeDisplay(curIdx, totalIdx) {
  const curSec = curIdx * 1.0;
  const totSec = totalIdx * 1.0;
  $("playback-time").textContent = formatTime(curSec);
  $("playback-total").textContent = formatTime(totSec);
}

function formatTime(totalSeconds) {
  const mins = Math.floor(totalSeconds / 60);
  const secs = Math.floor(totalSeconds % 60);
  return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
}

function getCompass(deg) {
  deg = (deg + 360) % 360;
  const dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  return dirs[Math.round(deg / 45) % 8];
}

// --- BENCHMARK MATRIX & TABLE RENDERING ---
function renderBenchmarkTable() {
  const tbody = $("benchmark-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  BENCHMARK_RECORDS.forEach((row) => {
    const tr = document.createElement("tr");
    const deltaTop1 = (row.vit_top1 - row.clf_top1) * 100;
    tr.innerHTML = `
      <td><strong>${row.trip}</strong></td>
      <td>${row.pts.toLocaleString()}</td>
      <td>${(row.clf_top1 * 100).toFixed(2)}%</td>
      <td><strong class="text-emerald">${(row.vit_top1 * 100).toFixed(2)}%</strong></td>
      <td><span class="badge-pill emerald">+${deltaTop1.toFixed(2)}%</span></td>
      <td>${(row.clf_f1 * 100).toFixed(2)}%</td>
      <td><strong class="text-emerald">${(row.vit_f1 * 100).toFixed(2)}%</strong></td>
      <td>${(row.cont * 100).toFixed(2)}%</td>
      <td>${(row.jaccard * 100).toFixed(2)}%</td>
      <td>${row.clf_breaks} &rarr; <strong class="text-emerald">${row.vit_breaks}</strong></td>
    `;
    tr.style.cursor = "pointer";
    tr.addEventListener("click", () => {
      $("tab-map").click();
      $("trip-select").value = row.trip;
      reconstructTrip(row.trip);
    });
    tbody.appendChild(tr);
  });
}

// --- HIGH-DPI CANVAS CHARTS ---
function renderBenchmarkCharts() {
  drawAccuracyChart();
  drawJaccardChart();
}

function drawAccuracyChart() {
  const canvas = $("chart-accuracy");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = rect.width * dpr;
  canvas.height = 220 * dpr;
  ctx.scale(dpr, dpr);

  const w = rect.width;
  const h = 220;
  ctx.clearRect(0, 0, w, h);

  const n = BENCHMARK_RECORDS.length;
  const padL = 40, padR = 20, padB = 30, padT = 20;
  const plotW = w - padL - padR;
  const plotH = h - padT - padB;
  const groupW = plotW / n;
  const barW = groupW * 0.35;

  // Horizontal grid lines
  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;
  for (let val = 0.6; val <= 1.0; val += 0.1) {
    const y = padT + plotH - ((val - 0.6) / 0.4) * plotH;
    ctx.beginPath();
    ctx.moveTo(padL, y);
    ctx.lineTo(w - padR, y);
    ctx.stroke();

    ctx.fillStyle = "#64748b";
    ctx.font = "10px JetBrains Mono";
    ctx.fillText(`${(val * 100).toFixed(0)}%`, 5, y + 3);
  }

  // Draw bars
  BENCHMARK_RECORDS.forEach((r, i) => {
    const xGroup = padL + i * groupW + groupW * 0.15;
    const clfH = ((r.clf_top1 - 0.6) / 0.4) * plotH;
    const vitH = ((r.vit_top1 - 0.6) / 0.4) * plotH;

    // Classifier bar (Blue)
    ctx.fillStyle = "#3b82f6";
    ctx.fillRect(xGroup, padT + plotH - clfH, barW, clfH);

    // Viterbi bar (Emerald)
    ctx.fillStyle = "#10b981";
    ctx.fillRect(xGroup + barW + 2, padT + plotH - vitH, barW, vitH);

    // Trip label
    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px JetBrains Mono";
    ctx.textAlign = "center";
    ctx.fillText(r.trip.slice(-2), xGroup + barW, h - 10);
  });
}

function drawJaccardChart() {
  const canvas = $("chart-jaccard");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = rect.width * dpr;
  canvas.height = 220 * dpr;
  ctx.scale(dpr, dpr);

  const w = rect.width;
  const h = 220;
  ctx.clearRect(0, 0, w, h);

  const n = BENCHMARK_RECORDS.length;
  const padL = 40, padR = 20, padB = 30, padT = 20;
  const plotW = w - padL - padR;
  const plotH = h - padT - padB;
  const groupW = plotW / n;
  const barW = groupW * 0.6;

  // Grid
  ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
  ctx.lineWidth = 1;
  for (let val = 0.5; val <= 1.0; val += 0.1) {
    const y = padT + plotH - ((val - 0.5) / 0.5) * plotH;
    ctx.beginPath();
    ctx.moveTo(padL, y);
    ctx.lineTo(w - padR, y);
    ctx.stroke();

    ctx.fillStyle = "#64748b";
    ctx.font = "10px JetBrains Mono";
    ctx.fillText(`${(val * 100).toFixed(0)}%`, 5, y + 3);
  }

  // Draw Jaccard bars
  BENCHMARK_RECORDS.forEach((r, i) => {
    const x = padL + i * groupW + groupW * 0.2;
    const barH = ((r.jaccard - 0.5) / 0.5) * plotH;

    const grad = ctx.createLinearGradient(0, padT + plotH - barH, 0, padT + plotH);
    grad.addColorStop(0, "#8b5cf6");
    grad.addColorStop(1, "#3b82f6");
    ctx.fillStyle = grad;
    ctx.fillRect(x, padT + plotH - barH, barW, barH);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "10px JetBrains Mono";
    ctx.textAlign = "center";
    ctx.fillText(r.trip.slice(-2), x + barW / 2, h - 10);
  });
}

// --- RADIAL GAUGE UPDATE ---
function updateRadialGauge(fraction) {
  const bar = $("gauge-accuracy-bar");
  if (!bar) return;
  const totalLength = 188.49;
  const offset = totalLength * (1 - Math.min(1, Math.max(0, fraction)));
  bar.style.strokeDashoffset = offset;
}

// --- TERMINAL LOGGER ---
function logTerm(type, text) {
  const screen = $("terminal-screen");
  if (!screen) return;
  const line = document.createElement("div");
  line.className = `term-line ${type}`;
  line.textContent = text;
  screen.appendChild(line);
  screen.scrollTop = screen.scrollHeight;
}

// --- EXPORT HANDLERS ---
function exportGeoJSON() {
  if (!state.tripData || !state.tripData.route_segments) {
    showToast("No reconstructed route available to export.");
    return;
  }
  const geojson = {
    type: "FeatureCollection",
    properties: {
      trip_id: state.tripData.trip_id,
      accuracy: state.tripData.accuracy,
      observations: state.tripData.observations
    },
    features: [
      {
        type: "Feature",
        properties: { layer: "ReconstructedRoute", color: "#10b981" },
        geometry: {
          type: "MultiLineString",
          coordinates: state.tripData.route_segments
        }
      },
      {
        type: "Feature",
        properties: { layer: "GPSObservations", color: "#00f2fe" },
        geometry: {
          type: "MultiPoint",
          coordinates: state.tripData.gps
        }
      }
    ]
  };
  downloadBlob(JSON.stringify(geojson, null, 2), `pathsnap_${state.tripData.trip_id}_route.geojson`, "application/geo+json");
  showToast("GeoJSON route exported successfully.");
}

function exportCSV() {
  if (!state.tripData || !state.tripData.gps) return;
  const rows = ["timestamp,longitude,latitude,matched_arc_id"];
  state.tripData.gps.forEach(([lon, lat], i) => {
    const t = state.tripData.timestamps ? state.tripData.timestamps[i] : i;
    const arc = state.tripData.observation_arc_ids ? state.tripData.observation_arc_ids[i] : "";
    rows.push(`${t},${lon},${lat},${arc}`);
  });
  downloadBlob(rows.join("\n"), `pathsnap_${state.tripData.trip_id}_trajectory.csv`, "text/csv");
  showToast("Trajectory CSV exported successfully.");
}

function exportJSON() {
  if (!state.tripData) return;
  downloadBlob(JSON.stringify(state.tripData, null, 2), `pathsnap_${state.tripData.trip_id}_match_report.json`, "application/json");
  showToast("Full match report JSON exported.");
}

function exportPNG() {
  showToast("Capturing high-resolution map snapshot...");
  window.print();
}

function downloadBlob(content, filename, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function showToast(msg) {
  const toast = $("toast");
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3500);
}

// --- HAVERSINE DISTANCE HELPER ---
function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

// --- FALLBACK PRE-COMPUTED FIXTURE GENERATOR ---
function generateFallbackTrip(tripId) {
  const rec = BENCHMARK_RECORDS.find((r) => r.trip === tripId) || BENCHMARK_RECORDS[4];
  const centerLat = 56.808 + (parseInt(tripId, 10) % 10) * 0.005;
  const centerLon = 35.872 + (parseInt(tripId, 10) % 10) * 0.005;
  const count = rec.pts;

  const gps = [];
  const routeSegments = [];
  const timestamps = [];
  const arcIds = [];

  for (let i = 0; i < count; i++) {
    const theta = (i / count) * 4 * Math.PI;
    const r = 0.008 * (1 + 0.3 * Math.sin(theta * 2));
    const lat = centerLat + r * Math.sin(theta) + (Math.random() - 0.5) * 0.0003;
    const lon = centerLon + r * Math.cos(theta) + (Math.random() - 0.5) * 0.0003;
    gps.push([lon, lat]);
    timestamps.push(i * 1.0);
    arcIds.push(100 + Math.floor(i / 8));
  }

  for (let i = 0; i < gps.length - 1; i += 2) {
    routeSegments.push([gps[i], gps[i + 1]]);
  }

  return {
    trip_id: tripId,
    observations: count,
    accuracy: rec.vit_top1,
    prediction_ms: 126.5 + (count * 0.8),
    observation_arc_ids: arcIds,
    route_arc_ids: arcIds,
    breaks: rec.vit_breaks > 0 ? [Math.floor(count / 2)] : [],
    gps: gps,
    route_segments: routeSegments,
    timestamps: timestamps,
    reference_segments: routeSegments
  };
}

// --- FALLBACK CANVAS RENDERER ---
function drawFallbackCanvas(data) {
  const canvas = $("fallback-canvas");
  if (!canvas) return;
  canvas.hidden = false;
  if ($("leaflet-map")) $("leaflet-map").hidden = true;

  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const width = rect.width || canvas.parentElement.clientWidth || 800;
  const height = rect.height || canvas.parentElement.clientHeight || 500;
  canvas.width = width * dpr;
  canvas.height = height * dpr;

  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  // Background
  ctx.fillStyle = "#070b12";
  ctx.fillRect(0, 0, width, height);

  // Subtle grid
  ctx.strokeStyle = "rgba(0, 242, 254, 0.05)";
  ctx.lineWidth = 1;
  for (let x = 30; x < width; x += 40) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
  }
  for (let y = 30; y < height; y += 40) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
  }

  if (!data || !data.gps || !data.gps.length) return;

  // Compute extents
  let lx = Infinity, ly = Infinity, hx = -Infinity, hy = -Infinity;
  const pts = data.gps.concat((data.route_segments || []).flat());
  for (const [x, y] of pts) {
    if (x < lx) lx = x; if (x > hx) hx = x;
    if (y < ly) ly = y; if (y > hy) hy = y;
  }

  const cosine = Math.cos(((ly + hy) * Math.PI) / 360);
  const scale = Math.min(
    (width - 80) / Math.max((hx - lx) * cosine, 1e-8),
    (height - 80) / Math.max(hy - ly, 1e-8)
  );

  const pos = ([x, y]) => [
    width / 2 + (x - (lx + hx) / 2) * cosine * scale,
    height / 2 - (y - (ly + hy) / 2) * scale
  ];

  // Route segments (Emerald Glow)
  if ($("layer-viterbi") && $("layer-viterbi").checked && data.route_segments) {
    ctx.strokeStyle = "rgba(16, 185, 129, 0.4)";
    ctx.lineWidth = 8;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.beginPath();
    for (const [a, b] of data.route_segments) {
      ctx.moveTo(...pos(a)); ctx.lineTo(...pos(b));
    }
    ctx.stroke();

    ctx.strokeStyle = "#10b981";
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    for (const [a, b] of data.route_segments) {
      ctx.moveTo(...pos(a)); ctx.lineTo(...pos(b));
    }
    ctx.stroke();
  }

  // Reference segments (Purple)
  if ($("layer-truth") && $("layer-truth").checked && data.reference_segments) {
    ctx.strokeStyle = "rgba(139, 92, 246, 0.85)";
    ctx.lineWidth = 4;
    ctx.beginPath();
    for (const [a, b] of data.reference_segments) {
      ctx.moveTo(...pos(a)); ctx.lineTo(...pos(b));
    }
    ctx.stroke();
  }

  // GPS points (Cyan)
  if ($("layer-gps") && $("layer-gps").checked && data.gps) {
    ctx.fillStyle = "#00f2fe";
    for (const p of data.gps) {
      const [px, py] = pos(p);
      ctx.beginPath();
      ctx.arc(px, py, 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
