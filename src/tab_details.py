#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# tab_details.py

import common

class DetailsTabManager(object):
    def __init__(self, glade, manager):
        self.manager = manager
        
        self.paused_unique_id = None
        
        # Look into glade's widget prefix function
        self.progress_bar = glade.get_widget("progressbar")
        self.name = glade.get_widget("summary_name")
        self.total_size = glade.get_widget("summary_total_size")
        self.num_files = glade.get_widget("summary_num_files")
        self.pieces = glade.get_widget("summary_pieces")
        self.availability = glade.get_widget("summary_availability")
        self.total_downloaded = glade.get_widget("summary_total_downloaded")
        self.total_uploaded = glade.get_widget("summary_total_uploaded")
        self.download_speed = glade.get_widget("summary_download_speed")
        self.upload_speed = glade.get_widget("summary_upload_speed")
        self.seeders = glade.get_widget("summary_seeders")
        self.peers = glade.get_widget("summary_peers")
        self.percentage_done = glade.get_widget("summary_percentage_done")
        self.share_ratio = glade.get_widget("summary_share_ratio")
        self.tracker = glade.get_widget("summary_tracker")
        self.tracker_status = glade.get_widget("summary_tracker_status")
        self.next_announce = glade.get_widget("summary_next_announce")
        self.eta = glade.get_widget("summary_eta")
        
    def update(self, unique_id):
        state = self.manager.get_torrent_state(unique_id)

        # Update selected files size, tracker, tracker status and next 
        # announce no matter what status of the torrent is
        self.total_size.set_text(common.fsize(state["total_wanted"]))
        self.tracker.set_text(str(state["tracker"]))
        # At this time we still may not receive EVENT_TRACKER so there
        # could be no tracker_status yet.
        if "tracker_status" in state:
            self.tracker_status.set_text(state["tracker_status"])
        self.next_announce.set_text(str(state["next_announce"]))
        
        if state['is_paused']:
            if not self.paused_unique_id:
                # Selected torrent just paused, zero data now and don't 
                # update it anymore on each update()
                state['num_seeds'] = state['total_seeds'] = \
                    state['num_peers'] = state['total_peers'] = \
                    state['download_rate'] = state['upload_rate'] = 0
                    
                self.paused_unique_id = unique_id
            elif self.paused_unique_id != unique_id:
                # User selected another paused torrent with unique_id after
                # paused torrent with self.paused_unique_id, so update
                # currently selected unique_id and do full update of details
                self.paused_unique_id = unique_id
            else:
                # If we already updated paused torrent - do nothing more
                return
        else:
            self.paused_unique_id = None
        
        self.name.set_text(state['name'])
        self.num_files.set_text(str(state['num_files']))
        self.pieces.set_text('%s x %s' % (state["num_pieces"], 
                                          common.fsize(state["piece_length"])))
        self.availability.set_text('%.3f' % state["distributed_copies"])
        self.total_downloaded.set_text('%s (%s)' % \
            (common.fsize(state["total_done"]),
             common.fsize(state["total_download"])))
        self.total_uploaded.set_text('%s (%s)' % \
            (common.fsize(self.manager.unique_IDs[unique_id].uploaded_memory+\
                          state["total_payload_upload"]),
             common.fsize(state["total_upload"])))
        self.download_speed.set_text(common.fspeed(state["download_rate"]))
        self.upload_speed.set_text(common.fspeed(state["upload_rate"]))
        self.seeders.set_text(common.fseed(state))
        self.peers.set_text(common.fpeer(state))
        self.progress_bar.set_fraction(float(state['progress']))
        self.progress_bar.set_text(common.fpcnt(state["progress"]))
        self.eta.set_text(common.estimate_eta(state))
        self.share_ratio.set_text( '%.3f' % self.manager.calc_ratio(unique_id, 
                                                                    state))
        
    def clear(self):
        self.name.set_text("")
        self.total_size.set_text("")
        self.num_files.set_text("")
        self.pieces.set_text("")
        self.availability.set_text("")
        self.total_downloaded.set_text("")
        self.total_uploaded.set_text("")
        self.download_speed.set_text("")
        self.upload_speed.set_text("")
        self.seeders.set_text("")
        self.peers.set_text("")
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_text("")
        self.share_ratio.set_text("")
        self.tracker.set_text("")
        self.tracker_status.set_text("")
        self.next_announce.set_text("")
        self.eta.set_text("")
        
