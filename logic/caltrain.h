#ifndef caltrain_H_
#define caltrain_H_

#include <project.h>
#ifdef CONFIG_CALTRAIN

// *************************************************************************************************
// Prototypes section
extern void start_caltrain(void);
extern void stop_caltrain(void);
extern void reset_caltrain(void);
extern u8 is_caltrain(void);
extern void caltrain_tick(void);
extern void update_caltrain_timer(void);
extern void mx_caltrain(u8 line);
extern void sx_caltrain(u8 line);
extern void display_caltrain(u8 line, u8 update);
extern void set_caltrain(void);

#define CALTRAIN_STOP				(0u)
#define CALTRAIN_RUN				(1u)
#define CALTRAIN_HIDE				(2u)

#endif // CONFIG_CALTRAIN
#endif // caltrain_H
